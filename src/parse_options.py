import argparse
import sys

def version(options):
    '''Prints the version information.
    '''

    print "{name}, version {version}\n".format(name=options['long_name'],
                                               version=options['version'])

def usage(options):
    '''Usage information.
    '''

    version (options)

    print '''\
usage: {} [-hvn] [-l log] [-u user]
         {} {} {}

Modify access to the TCC database services. This only works on Mac OS X 10.8 or
later!

    h : prints this help message
    v : prints the version information
    n : prevents logs from being written to file and enables console output

    l log    : use 'log' as the logging output location
    u user   : change settings for 'user'
    d darwin : set the Darwin version manually
               (12 for OS X 10.8, 13 for OS X 10.9)

'ACTION'
    add    : add applications to the service
    remove : remove applications from the service

'SERVICE'
    contacts      : modifies access to Address Book
    icloud        : modifies access to iCloud services (not often used)
    accessibility : modifies access to system Accessibility settings

    Note that modifying the Accessibility settings requires root access.

'APPLICATIONS'
    The names of applications can be specified in these ways:

    shortname   : e.g. 'safari'                   'myapp'
    bundle ID   : e.g. 'com.apple.Safari'         'com.mystuff.MyApp'
    bundle path : e.g. '/Applications/Safari.app' '/Path/to/MyApp.app'

    You can modify settings for multiple applications at a time.\
'''.format(options['name'], '{action}', '{service}', '{applications}')
    sys.exit(0)

def parse(options):
    '''Parses the options given to the script.
    '''

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help',
                        action='store_true')
    parser.add_argument('-v', '--version',
                        action='store_true')
    parser.add_argument('-n', '--no-log',
                        action='store_true')
    parser.add_argument('-l', '--log')
    parser.add_argument('-u', '--user',
                        default='')
    parser.add_argument('-d', '--darwin', type=int)
    parser.add_argument('action',
                        nargs='?',
                        choices=['add', 'remove'],
                        default=None)
    parser.add_argument('service',
                        nargs='?',
                        choices=['contacts', 'accessibility', 'icloud'],
                        default=None)
    parser.add_argument('apps',
                        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.help:
        usage(options)
    if args.version:
        version(options)
        sys.exit(0)
    options['log'] = not args.no_log
    options['log_dest'] = args.log
    options['user'] = args.user
    if args.darwin:
        options['darwin'] = args.darwin
    if not args.action:
        print "Error: You must specify an action!"
        sys.exit(5)
    options['action'] = args.action
    if not args.service:
        print "Error: You must specify a service!"
        sys.exit(5)
    options['service'] = args.service
    if not args.apps:
        print "Error: You must specify at least one application!"
        sys.exit(5)
    options['apps'] = args.apps
