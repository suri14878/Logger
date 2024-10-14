import logging, os, configparser, datetime

# function to create config file for logger
def CreateLoggerConfig(config_filename = "./Configs/Logger.ini"):
    try:
        print(f"Attempting to create Logger config file '{config_filename}'...")

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
        MakeDirectory(config_filename)
        with open(config_filename, 'w') as configfileObj:
            config.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()

        print(f"Config file '{config_filename}' created.")
    except Exception as e:
        print(f"Exception creating logger config file: {e}")

def MakeDirectory(file_path):
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory) and len(directory) > 0:
            print(f"Directory {directory} did not exist, creating it.")
            os.makedirs(directory)
        return True
    except Exception as e:
        print(f"Exception creating directory: {e}")
        return False

# function to read configurations file
def ReadLoggerConfig(file_path = "./Configs/Logger.ini"):
    try:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config
    except Exception as e:
        return None
    
# function to create a logger
def create_logger(ConfigFilePath = None, OverwriteRoot=False):
    if ConfigFilePath is None:
        config = ReadLoggerConfig()
    else:
        config = ReadLoggerConfig(file_path=ConfigFilePath)

    file_path = config['Logger Settings']['FilePath']
    file_name = config['Logger Settings']['FileName']
    extension = config['Logger Settings']['Extension']
    include_timestamp = config['Logger Settings']['IncludeTimestamp']
    overwrite = config['Logger Settings']['Overwrite']
    consoleOutput = config['Logger Settings']['ConsoleOutput']
    log_level = config['Logger Settings']['LogLevel']

    # Creates directory for logger if it doesn't exist
    MakeDirectory(file_path)
    
    # Adds special timestamp formatting
    if(include_timestamp == 'TRUE'):
        now = datetime.now()
        log_file = file_path + file_name + now.strftime(r" %m.%d.%Y %H.%M.%S") + extension
    else:
        log_file = file_path + file_name + extension
    

    # Checks if create_logger() is called multiple times.
    removed_handlers = False
    root_handler_count = len(logging.root.handlers)
    if root_handler_count > 0:
        if OverwriteRoot:
            logging.warning(f"create_logger(OverwriteRoot = True) was called with {root_handler_count} handlers already existing.")
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            removed_handlers = True
        else:
            logging.warning(f"{root_handler_count} handlers exist on root logging object already, ignoring create_logger() call. If you want to re-define the handler objects, use the OverwriteRoot = True parameter")
            return logging
    
    # Sets up relevent handlers for file output and console output if specified. If removed handlers in this call, set to append so we don't lose logger history in a single execution.
    handlers = [logging.FileHandler(log_file, mode=f"{'w' if (overwrite=='TRUE' and not removed_handlers) else 'a'}")]
    if(consoleOutput == 'TRUE'):
        handlers.append(logging.StreamHandler())

    logging.basicConfig(level=log_level, 
                        handlers=handlers,
                        format=r'%(asctime)s [%(levelname)s] [%(name)s]: %(message)s', 
                        datefmt=r'%m/%d/%Y %I:%M:%S %p'
                    )
    return logging