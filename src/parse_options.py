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
    parser.add_argument('service',
                        choices=['contacts', 'accessibility', 'icloud', 'help'])
    parser.add_argument('action',
                        choices=['add', 'remove'])
    parser.add_argument('app',
                        nargs=argparse.REMAINDER)
    parser.add_argument('-l', '--log')
    parser.add_argument('-n', '--no-log',
                        action='store_false')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='TCC Database Manager ' + options['version'])
    args = parser.parse_args()

    # Consider adding sub-helps for each service?
    # Brief description or something?
    if args.services = "help":
        usage(options['name'])
    options['service'] = args.services
    options['action'] = args.action
    options['app'] = args.app
    options['log_dest'] = args.log
    options['log'] = args.no_log
