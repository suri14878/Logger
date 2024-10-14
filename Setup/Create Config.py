import sys, os, importlib

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import src.Logger as Logger

def CreateConfigs():
    try:
        Logger.CreateLoggerConfig()
        logging = Logger.create_logger()
        logger = logging.getLogger("Create Configs")
        logger.info("Sucessfully created logger and associated config.")
    except Exception as e:
        print(f"Exception when setting up logger and associated config: {e}")

if __name__ == "__main__":
    CreateConfigs()
