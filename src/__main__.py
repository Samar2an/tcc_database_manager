import os
import parse_options
import sys

from helpful_tools.app_info import AppInfo
from tcc_edit import TCCEdit

def set_globals ():
    '''Global options are set here.
    '''

    global options
    options = {}
    options['long_name'] = 'TCC Database Manager'
    options['name'] = '_'.join(options['long_name'].lower().split())
    options['version'] = '3.0'

def setup_logger ():
    '''Creates the logger to be used throughout, after first checkign that the
    Management Logger package has been installed.
    '''

    # Check that the logging imports properly.
    try:
        from management_logging import loggers
    except ImportError, e:
        print "You need the 'Management Logging' module to be installed first."
        print "https://github.com/univ-of-utah-marriott-library-apple/management_logging"
        print
        print "You can use the '-n' switch to ignore this:"
        print "  $ location_services_manager -n ..."
        sys.exit(3)

    global logger
    if options['log']:
        # A logger!
        if not options['log_dest']:
            logger = loggers.file_logger(options['name'])
        else:
            logger = loggers.file_logger(options['name'], path=options['log_dest'])
    else:
        # A dummy logger.  It won't record anything.
        logger = loggers.stream_logger(0)

def main ():
    set_globals()
    parse_options.parse(options)
    # setup_logger()

    bids = []
    for app in options['apps']:
        bids.append(AppInfo(app).bid)

    print bids
    return

    if options['action'] == "add":
        with TCCEdit(options['user']) as e:
            for bid in bids:
                logger.info("Adding '" + bid + "' to " + options['service'] + " service.")
                e.insert(options['service'], bid)
    else:
        with TCCEdit(options['user']) as e:
            for bid in bids:
                logger.info("Removing '" + bid + "' from " + options['service'] + " service.")
                e.remove(options['service'], bid)

if __name__ == "__main__":
    main()
