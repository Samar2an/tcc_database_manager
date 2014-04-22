import os
import parse_options
import sys

def set_globals ():
    '''Global options are set here.
    '''

    global options
    options = {}
    options['long_name'] = 'TCC Database Manager'
    options['name'] = '_'.join(options['long_name'].lower().split())
    options['version'] = '3.0'
    options['local_dir'] = os.path.expanduser('~/Library/Application Support/com.apple.TCC')
    options['local_db'] = os.path.join(options['local_dir'], 'TCC.db')
    options['root_dir'] = '/Library/Application Support/com.apple.TCC'
    options['root_db'] = os.path.join(options['root_dir'], 'TCC.db')

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



if __name__ == "__main__":
    main()
