import os
import parse_options
import sys

from tcc_edit import TCCEdit

# Check that the logging imports properly.
try:
    from helpful_tools.app_info import AppInfo
    from helpful_tools import loggers
except ImportError, e:
    print "You need the 'Helpful Tools' module to be installed first."
    print "https://github.com/univ-of-utah-marriott-library-apple/helpful_tools"
    print
    print "You can use the '-n' switch to ignore this:"
    print "  $ location_services_manager -n ..."
    sys.exit(3)

def set_globals ():
    '''Global options are set here.
    '''

    global options
    options = {}
    options['long_name'] = 'TCC Database Manager'
    options['name'] = '_'.join(options['long_name'].lower().split())
    options['version'] = '3.1'

def setup_logger ():
    '''Creates the logger to be used throughout.

    If it was not specified not to create a log, the log will be created in either
    the default location (as per helpful_tools) or a specified location.

    Otherwise, the logger will just be console output.
    '''

    global logger
    if options['log']:
        # A logger!
        if not options['log_dest']:
            logger = loggers.file_logger(options['name'])
        else:
            logger = loggers.file_logger(options['name'], path=options['log_dest'])
    else:
        # A dummy logger.  It won't record anything to file.
        logger = loggers.stream_logger(1)

def main ():
    set_globals()
    parse_options.parse(options)
    setup_logger()

    bids = []
    for app in options['apps']:
        bids.append(AppInfo(app).bid)

    logger.info("Found bundle IDs: " + str(bids))

    if options['action'] == "add":
        with TCCEdit(options['user']) as e:
            for bid in bids:
                if options['user']:
                    logger.info("Adding '" + bid + "' to " + options['service'] + " service for " + options['user'] + ".")
                else:
                    logger.info("Adding '" + bid + "' to " + options['service'] + " service.")
                e.insert(options['service'], bid)
    else:
        with TCCEdit(options['user']) as e:
            for bid in bids:
                if options['user']:
                    logger.info("Adding '" + bid + "' to " + options['service'] + " service for " + options['user'] + ".")
                else:
                    logger.info("Adding '" + bid + "' to " + options['service'] + " service.")
                e.remove(options['service'], bid)

if __name__ == "__main__":
    main()
