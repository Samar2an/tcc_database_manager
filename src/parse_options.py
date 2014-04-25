import argparse
import sys

def usage (name):
    '''Gives useful usage information.
    '''

    print "This is some helpful information.  Maybe."

def parse (options):
    '''Parses the options given to the script.
    '''

    parser = argparse.ArgumentParser(description="Can add or remove applications from the various TCC databases: Contacts, Accessbility, and iCloud.",
                                     add_help=False)
    parser.add_argument('action',
                        choices=['add', 'remove', 'help'])
    parser.add_argument('service',
                        nargs='?',
                        choices=['contacts', 'accessibility', 'icloud'],
                        default=None)
    parser.add_argument('apps',
                        nargs=argparse.REMAINDER)
    parser.add_argument('-l', '--log')
    parser.add_argument('-n', '--no-log',
                        action='store_true')
    parser.add_argument('-u', '--user',
                        default='')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=options['long_name'] + ' ' + options['version'])
    args = parser.parse_args()

    # Consider adding sub-helps for each service?
    # Brief description or something?
    if args.action == "help":
        usage(options['name'])
    options['action'] = args.action
    if not args.service:
        print "You must specify a service!"
        sys.exit(5)
    options['service'] = args.service
    if not args.apps:
        print "You must specify at least one application!"
        sys.exit(5)
    options['apps'] = args.apps
    options['log_dest'] = args.log
    options['log'] = not args.no_log
    options['user'] = args.user
