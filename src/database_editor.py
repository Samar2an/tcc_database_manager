import os
import sqlite3

class TCCEdit:
    def __init__(self, options):
        self.root = sqlite3.connect(options['root_db'])
        self.local = sqlite3.connect(options['local_db'])

    def insert(self, service, bid):
        service = service.lower()
        if not service in ['accessibility', 'contacts', 'icloud']:
            raise ValueError("Invalid service provided.")

        if service == 'accessibility':
            connection = self.root
        elif service == 'contacts':
            connection = self.local
        elif service == 'icloud':
            connection = self.local

        c = connection.cursor()

        c.execute("INSERT or REPLACE into access values('"
                    + service + "', '" + bid
                    + "', 0, 1, 0, NULL)")
        connection.commit()

    def remove(self, service, bid):
        pass

    # Need a tear-down method.
