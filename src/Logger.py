import logging, os, configparser, datetime
from pathlib import Path

default_config_path = "./Configs/Logger.ini"

def create_root(ConfigFilePath:Path = None, LogRelativeToConfig:Path=None, OverwriteRoot:bool = False):
    """
    This method should be called prior to creating any loggers and typically must only be called once. 
    Attempts to set up the root service so that you can build out multiple loggers. 

    Parameters:
            ConfigFilePath (Path): The filepath to the logger configuration file. 
                If unspecified, it will default to "./Configs/Logger.ini". 
                If it doesn't already exist, it will attempt to create it.
            LogRelativeToConfig (Path): By default, the logger's output location will be based on a relative or absolute path provided in the config file.
                Depending on how this method is called, that relative path may be interpretted locally (Usually this occurs if you're utilizing the logger from multiple services)
                Changing this parameter to will ensure the log file is saved relative to the config location.
                If the config is saved in a "./Configs/" subfolder, then passing "../" will save it in the base folder in a similar to default behavior.
            OverwriteRoot (bool): By default once a root is created this method will not attempt to re-create the root logger.
                Changing this to True will allow this method to overwrite the root handler. Utilizing this may result in loss of previously logged messages,
                especially if you're writing to the same log location after the overwrite.
                Use this if you're needing to modify and update logger settings in the middle of program execution.
    """
    try:
        # Checks if create_logger() is called multiple times.
        removed_handlers = False
        root_handler_count = __getRootHandlerCount()
        if root_handler_count > 0:
            if OverwriteRoot:
                __SafeLogging('warning', f"create_logger(OverwriteRoot = True) was called with {root_handler_count} handlers already existing.")
                __SafeLogging('warning', f"This is my last message before killing handlers. Future messages may not be logged.")
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)
                removed_handlers = True
            else:
                __SafeLogging('warning', f"{root_handler_count} handlers exist on root logging object already, ignoring create_logger() call. If you want to re-define the handler objects, use the OverwriteRoot = True parameter")
                return logging
        
        # Attempts to read logger config file
        if ConfigFilePath is None:
            ConfigFilePath = default_config_path
        config = __ReadConfig(file_path=ConfigFilePath)

        # If we are missing the default config file and expected it, then try to automatically create it and recover.
        if config is None and ConfigFilePath == default_config_path:
            __SafeLogging('info', "Default logger config expected was not found. Attempting to create it.")
            __CreateDefaultConfig(config_filename = ConfigFilePath)
            config = __ReadConfig(file_path = ConfigFilePath)

        file_path = config['Logger Settings']['FilePath']
        file_name = config['Logger Settings']['FileName']
        extension = config['Logger Settings']['Extension']
        include_timestamp = config['Logger Settings']['IncludeTimestamp']
        overwrite = config['Logger Settings']['Overwrite']
        consoleOutput = config['Logger Settings']['ConsoleOutput']
        log_level = config['Logger Settings']['LogLevel']
        
        if LogRelativeToConfig is not None:
            if(Path(file_path).is_absolute()):
                __SafeLogging('warning', "LogRelativeToConfig paremeter specified for an absolute path. Expected a relative path for logger FilePath only.")
                __SafeLogging('warning', f"Using path: {file_path}")
            elif not os.path.exists(LogRelativeToConfig):
                __SafeLogging('warning', "LogRelativeToConfig paremeter is not a path object. Expected a relative path in this parameter.")
                __SafeLogging('warning', f"Using path: {file_path}")
            elif Path(LogRelativeToConfig).is_absolute() or not LogRelativeToConfig.startswith("."):
                __SafeLogging('warning', "LogRelativeToConfig paremeter specified as an absolute path. Expected a relative path that starts with '.' in this parameter.")
                __SafeLogging('warning', f"Using path: {file_path}")
            else:
                 # set filepath to be relative to the config's parent directory.
                config_absolute = os.path.abspath(ConfigFilePath)
                parent_directory = os.path.dirname(config_absolute)
                file_path = os.path.abspath(os.path.join(parent_directory, LogRelativeToConfig, file_path))
                file_path = os.path.join(file_path, "") # This appends a final "\" to set it as a directory.
                __SafeLogging('info', f"Logging using modified relative path: {file_path}")

        # Creates directory for logger if it doesn't exist
        __MakeDirectory(file_path)
        
        # Adds special timestamp formatting
        if(include_timestamp == 'TRUE'):
            now = datetime.now()
            log_file = file_path + file_name + now.strftime(r" %m.%d.%Y %H.%M.%S") + extension
        else:
            log_file = file_path + file_name + extension
        
        # Sets up relevent handlers for file output and console output if specified. If removed handlers in this call, set to append so we don't lose logger history in a single execution.
        handlers = [logging.FileHandler(log_file, mode=f"{'w' if (overwrite=='TRUE' and not removed_handlers) else 'a'}")]
        if(consoleOutput == 'TRUE'):
            handlers.append(logging.StreamHandler())

        logging.basicConfig(level=log_level, 
                            handlers=handlers,
                            format=r'%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', 
                            datefmt=r'%m/%d/%Y %I:%M:%S %p'
                        )
        __SafeLogging("debug", "Logger sucessfully created and outputing results.")
        
    except Exception as e:
        __SafeLogging('error', f"Exception while setting up logger: {e}")
    finally:
        return logging

def create_logger(**kwargs):
    '''Deprecated function. Please utilize create_root() for clarity.'''
    __SafeLogging('warning', 'The create_logger() function is deprecated. Please utilize create_root() for clarity.')
    create_root(**kwargs)

def __CreateDefaultConfig(config_filename = default_config_path):
    ''' Creates default config for logger. Used internally.
    '''
    try:
        __SafeLogging('info', f"Attempting to create Logger config file '{config_filename}'...")

        # create config object
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str

        # Adds new section and settings for logger behavior
        config["Logger Settings"]={
            "# Save path for the log file, the log file name, and the log file extension": None,
            "FilePath": "./Logs/",
            "FileName" : "Log File",
            "Extension": ".log",
            "# Whether or not to include a timestamp in the log file name. Value of TRUE includes, FALSE excludes.": None,
            "IncludeTimestamp" : "FALSE",
            "# If not using timestamps, log files will go to a single file. This option controls if want the file to be overwritten each run. Appends data if not.": None,
            "Overwrite" : "TRUE",
            "# Sets whether logfile should be sent to console as well as log file": None,
            "ConsoleOutput" : "TRUE",
            '# Log level defines behavior of logging file and which messages are included.': None,
            '# DEBUG - Detailed information, typically of interest only when diagnosing problems.': None,
            '# INFO - Confirmation that things are working as expected.': None,
            '# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.': None,
            '# ERROR - Due to a more serious problem, the software has not been able to perform some function.': None,
            '# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.': None,
            "LogLevel" : "DEBUG",
            }
        
        # Make directory and save file
        __MakeDirectory(config_filename)
        with open(config_filename, 'w') as configfileObj:
            config.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()

        __SafeLogging('info', f"Config file '{config_filename}' created.")
    except Exception as e:
        __SafeLogging('error', f"Exception creating logger config file: {e}")

def __MakeDirectory(file_path):
    '''Used internally to create the directory of config files. 
    '''
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory) and len(directory) > 0:
            __SafeLogging('info', f"Directory {os.path.abspath(directory)} did not exist, creating it.")
            os.makedirs(directory)
        return True
    except Exception as e:
        __SafeLogging('error', f"Exception creating directory: {e}")
        return False

def __ReadConfig(file_path = default_config_path):
    '''Used internally to read the config file.
    '''
    try:
        __SafeLogging('info', f"Attempting to read config file {file_path}" )
        config = configparser.ConfigParser()
        dataset = config.read(file_path)
        if len(dataset) == 0:
            raise ValueError("Failed to open/find config files")
        return config
    except Exception as e:
        __SafeLogging('error', f"Failed to read config file {file_path}")
        return None

def __getRootHandlerCount():
    '''Gets the number of existing handlers on the root logger. Used internally.'''
    return len(logging.root.handlers)

def __SafeLogging(detail_level, message):
    '''Manages appropriate output for internal processes of the logger module.
    If it has not been created, then internal output goes to console only by default. 
    '''
    if __getRootHandlerCount() > 0:
        match detail_level:
            case 'debug':
                logging.debug(message)
            case 'info':
                logging.info(message)
            case 'warning':
                logging.warning(message)
            case 'error':
                logging.error(message)
            case _:
                logging.info(message)
    else:
        print(f"[{detail_level.upper()}] [Logger Module]: {message}")
