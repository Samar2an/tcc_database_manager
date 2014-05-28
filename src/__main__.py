import os
import parse_options
import sys

from tcc_edit import TCCEdit

# Check that the logging imports properly.
try:
    from management_tools.app_info import AppInfo
    from management_tools import loggers
except ImportError, e:
    print "You need the 'Management Tools' module to be installed first."
    print "https://github.com/univ-of-utah-marriott-library-apple/management_tools"
    sys.exit(3)

def set_globals():
    '''Global options are set here.
    '''

    global options
    options = {}
    options['long_name'] = 'TCC Database Manager'
    options['name'] = '_'.join(options['long_name'].lower().split())
    options['version'] = '3.2.0'

def setup_logger():
    '''Creates the logger to be used throughout.

    If it was not specified not to create a log, the log will be created in either
    the default location (as per management_tools) or a specified location.

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

def main():
    set_globals()
    parse_options.parse(options)
    setup_logger()
    check_osx_version()

    bids = []
    for app in options['apps']:
        bids.append(AppInfo(app).bid)

    logger.info("Found bundle IDs: " + str(bids))

    if options['action'] == "add":
        try:
            with TCCEdit(options['user'], options['darwin']) as e:
                for bid in bids:
                    if options['user']:
                        logger.info("Adding '" + bid + "' to " + options['service'] + " service for " + options['user'] + ".")
                    else:
                        logger.info("Adding '" + bid + "' to " + options['service'] + " service.")
                    e.insert(options['service'], bid)
        except:
            # There was an error!
            logger.error(sys.exc_info()[1].message)
            sys.exit(7)
    else:
        try:
            with TCCEdit(options['user'], options['darwin']) as e:
                for bid in bids:
                    if options['user']:
                        logger.info("Removing '" + bid + "' from " + options['service'] + " service for " + options['user'] + ".")
                    else:
                        logger.info("Removing '" + bid + "' from " + options['service'] + " service.")
                    e.remove(options['service'], bid)
        except:
            # There was an error!
            logger.error(sys.exc_info()[1].message)
            sys.exit(7)

def check_osx_version():
    if not 'darwin' in options:
        options['darwin'] = os.uname()[2].split('.')[0]
    options['darwin'] = int(options['darwin'])
    if options['darwin'] < 12:
        logger.error("There is no TCC database on this version of OS X. (Darwin v. " + str(options['darwin']) + ")")
        sys.exit(13)


if __name__ == "__main__":
    main()
