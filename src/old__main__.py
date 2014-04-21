'''
################################################################################

tcc_database_manager

    This script takes in a service name and a bundle ID and adds an entry to the
    appropriate TCC.db file to allow access for that item.  This is to be used
    to reduce the amount of dialogs gotten by users in our computer labs.

################################################################################

DETAILED USAGE INSTRUCTIONS

Usage: tcc_database_manager [-h] serviceName bundleID

    -h --help
        Prints this help and quits.  Takes precedence over any other options
        (but this must be the first option given).

    serviceName
        The short name for whatever service is being added to the TCC.db file.
        Valid options are:
            kTCCServiceAddressBook      (Contacts)
            kTCCServiceAccessibility    (Accessibility) - Requires root!
            kTCCServiceUbiquity         (iCloud)

    bundleID
        The bundle identifier for whatever program is to be added to the TCC.db
        file.  These generally look like (for example):
            com.apple.Finder

    NOTE: Any additional arguments past the two are thrown out.  There shouldn't
        be any instances where you would need spaces, but if you do put them
        into quotes.

################################################################################

COPYRIGHT (c) 2014 Marriott Library IT Services.  All Rights Reserved.

Author:          Pierce Darragh - pierce.darragh@utah.edu
Creation Date:   March 26, 2014
Last Updated:    April 10, 2014

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appears in all copies and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of The Marriott Library not be used in advertising or publicity
pertaining to distribution of the software without specific, written prior
permission. This software is supplied as-is without expressed or implied
warranties of any kind.

################################################################################
'''
import os
import sqlite3
import sys

from log_stuff import build_logger

def usage ():
    print '''
Usage: {0} [-h] serviceName bundleID

    -h --help
        Prints this help and quits.  Takes precedence over any other options
        (but this must be the first option given).

    serviceName
        The short name for whatever service is being added to the TCC.db file.
        Valid options are:
            kTCCServiceAddressBook      (Contacts)
            kTCCServiceAccessibility    (Accessibility) - Requires root!
            kTCCServiceUbiquity         (iCloud)

    bundleID
        The bundle identifier for whatever program is to be added to the TCC.db
        file.  These generally look like (for example):
            com.apple.Finder

    NOTE: Any additional arguments past the two are thrown out.  There shouldn't
        be any instances where you would need spaces, but if you do put them
        into quotes.
'''.format(options['name'])

def set_log_location ():
    '''Sets the logging location dynamically.  Prefers /var/log/tcc_database_manager.log,
    but will resort to ~/.logs/tcc_database_manager.log
    '''

    if os.path.exists("/var/log") and os.access("/var/log", os.W_OK):
        options['log_dest'] = "/var/log/" + options['name'] + ".log"
    else:
        home = os.path.expanduser('~')
        if not os.path.exists(home + "/.logs"):
            os.makedirs(home + "/.logs")
        options['log_dest'] = str(home) + "/.logs/" + options['name'] + ".log"

    # The same logger can now be used throughout.  Huzzah!
    global logger
    logger = build_logger(destination=options['log_dest'], name=options['name'])
    logger.setLevel(20) # A hard number is used so we don't have to import the whole logging module here.

def create_DB (path):
    logger.info("No database found at '" + path + "'.  Creating.")
    conn = sqlite3.connect(path)
    c = conn.cursor()

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
    conn.commit()
    conn.close()
    logger.info("Database created and initialized.")

def modify_DB ():
    if options['service_name'] == "kTCCServiceAddressBook":
        options['dir'] = options['local_dir']
        options['db'] = options['local_db']
    elif options['service_name'] == "kTCCServiceAccessibility":
        # Editing this TCC database requires administrative privileges.
        if os.geteuid() != 0:
            print "Must be run as root!"
            logger.error("Must run as root to modify Accessibility settings!")
            sys.exit(10)
        options['dir'] = options['root_dir']
        options['db'] = options['root_db']
    elif options['service_name'] == "kTCCServiceUbiquity":
        options['dir'] = options['local_dir']
        options['db'] = options['local_db']
    else:
        print "Invalid service name:", options['service_name']
        logger.error("Invalid service name: " + options['service_name'])
        return

    if options['dir'] and options['db']:
        print "Adding", options['bundle_id'], "to service", options['service_name'], "at", options['db']
        logger.info("Adding '" + options['bundle_id'] + "' to service " + options['service_name'])

        db_exists = False
        if not os.path.exists(options['dir']):
            os.mkdir(options['dir'], int('700', 8))
        else:
            if os.path.exists(options['db']):
                db_exists = True

        if not db_exists:
            create_DB (options['db'])

        conn = sqlite3.connect(options['db'])
        c = conn.cursor()

        c.execute("INSERT or REPLACE into access values('"
                   + options['service_name'] + "', '" + options['bundle_id']
                   + "', 0, 1, 0, NULL)")
        conn.commit()
        conn.close()
        logger.info("Entry successfully added.")

def automated ():
    logger.info("Running automated.")
    return
    # Add anything here you would like to have happen if the script is run without any arguments.

def main (argv):
    # Defaults
    global options
    options = {}
    options['name'] = "tcc_database_manager"
    options['service_name'] = None
    options['bundle_id'] = None
    options['local_dir'] = os.path.expanduser('~/Library/Application Support/com.apple.TCC')
    options['local_db'] = os.path.join(options['local_dir'], 'TCC.db')
    options['root_dir'] = os.path.expanduser('/Library/Application Support/com.apple.TCC')
    options['root_db'] = os.path.join(options['root_dir'], 'TCC.db')
    options['dir'] = None
    options['db'] = None
    set_log_location()

    # If we receive no options, pass execution along to the automation function.
    # This is used by us to handle automated execution of this script.
    if len(argv) < 2:
        automated()
        sys.exit(0)
    # If the user only specified one option, it had better be to ask for help.
    elif argv[1] == '--help' or argv[1] == 'help' or argv[1] == 'h' or argv[1] == '-h':
        usage()
        sys.exit(0)
    # Otherwise, the user should have specified at two options: one for the service name,
    # and one for the bundle ID to add.
    else:
        if len(argv) >= 3:
            options['service_name'] = argv[1]
            options['bundle_id'] = argv[2]
        else:
            print "Invalid arguments:",
            for i in range (1, len(argv)):
                print argv[i],
            print
            logger.error("Invalid arguments given.")
            sys.exit(2)

    if options['service_name'] and options['bundle_id']:
        modify_DB()
    else:
        print "Invalid arguments,"
        for i in range (1, len(argv)):
            print argv[i],
        print
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv)

