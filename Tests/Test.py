import os,sys

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import src.Logger as Logger

logging = Logger.create_root()
logging = Logger.create_root(LogRelativeToConfig="../")

def TestFunc1():
    logger = logging.getLogger("TestFunc1")
    logger.info("Output1")

def TestFunc2():
    logger = logging.getLogger("TestFunc2")
    logger.info("Output2")