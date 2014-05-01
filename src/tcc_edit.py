import os
import sqlite3

class TCCEdit:
    '''A class to help with editing the TCC databases.

    This ought to be used in a with statement to ensure proper closing of connections!
    '''

    def __init__(self, user=''):
        # These are the locations of the databases.
        self.root_path = '/Library/Application Support/com.apple.TCC/TCC.db'
        self.local_path = os.path.expanduser('~' + user + '/Library/Application Support/com.apple.TCC/TCC.db')

        # Check the user didn't supply a bad username.
        if not self.local_path.startswith('/'):
            raise ValueError("Invalid username supplied: " + user)

        if not os.access(self.local_path, os.W_OK):
            raise ValueError("You do not have permission to modify " + user + "'s TCC database.")

        # Ensure the databases exist properly.
        if os.access(self.root_path, os.W_OK) and not os.path.exists(self.root_path):
            self.__create(self.root_path)
        if not os.path.exists(self.local_path):
            self.__create(self.local_path)

        # Create the connections.
        if os.geteuid() == 0:
            self.root = sqlite3.connect(self.root_path)
        else:
            self.root = None
        self.local = sqlite3.connect(self.local_path)

        # The services have particular names and databases.
        self.services = {}
        self.services['accessibility'] = ('kTCCServiceAccessibility', self.root)
        self.services['contacts'] = ('kTCCServiceAddressBook', self.local)
        self.services['icloud'] = ('kTCCServiceUbiquity', self.local)

    def __enter__(self):
        return self

    def insert(self, service, bid):
        '''Adds the specified bundle identifer to the specified service.
        '''

        service = service.lower()
        if not service in self.services.keys():
            raise ValueError("Invalid service provided: " + service)

        connection = self.services[service][1]

        if not connection:
            raise ValueError("Must be root to modify this service!")

        c = connection.cursor()

        c.execute("INSERT or REPLACE into access values("
                    + "'" + self.services[service][0] + "', "
                    + "'" + bid + "', 0, 1, 0, NULL)")
        connection.commit()

    def remove(self, service, bid):
        '''Removes the specified bundle identifer from the specified service.
        '''

        service = service.lower()
        if not service in self.services.keys():
            raise ValueError("Invalid service provided: " + service)

        connection = self.services[service][1]

        if not connection:
            raise ValueError("Must be root to modify this service!")

        c = connection.cursor()

        c.execute("DELETE FROM access WHERE service IS "
                    + "'" + self.services[service][0] + "'"
                    + " AND client IS '" + bid + "'")
        connection.commit()

    def __create(self, path):
        '''Creates a database in the event that it does not already exist.

        These databases are formatted in a particular way.  Don't change this.
        '''

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path), int('700', 8))

        connection = sqlite3.connect(path)
        c = connection.cursor()

        c.execute('''CREATE TABLE admin
                     (key TEXT PRIMARY KEY NOT NULL, value INTEGER NOT NULL)''')
        c.execute("INSERT INTO admin VALUES ('version', 7)")
        c.execute('''CREATE TABLE access
                     (service TEXT NOT NULL,
                        client TEXT NOT NULL,
                        client_type INTEGER NOT NULL,
                        allowed INTEGER NOT NULL,
                        prompt_count INTEGER NOT NULL,
                        csreq BLOB,
                        CONSTRAINT key PRIMARY KEY (service, client, client_type))''')
        c.execute('''CREATE TABLE access_times
                     (service TEXT NOT NULL,
                        client TEXT NOT NULL,
                        client_type INTEGER NOT NULL,
                        last_used_time INTEGER NOT NULL,
                        CONSTRAINT key PRIMARY KEY (service, client, client_type))''')
        c.execute('''CREATE TABLE access_overrides
                     (service TEXT PRIMARY KEY NOT NULL)''')
        connection.commit()
        connection.close()

    def __exit__(self, type, value, traceback):
        '''This handles the closing of connections when the object is closed.

        If the object is put inside a with statement (as suggested above), this
        will be called automatically when the with is left.
        '''

        if self.root:
            self.root.close()
        self.local.close()
