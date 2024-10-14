# Logger Package

## Introduction
This project wraps the default python logging library to make it easier to work with and standarizes output options for internal projects.

## How to use the project
Follow this section if you are looking to user the Logger class in other projects.

### Include in requirements.txt to pip install:
To include the project, add the following line to your requirements.txt. You will have to be logged into your git account on the host machine.
```
Logger @ git+https://github.com/ULL-IR-Office/Logger@main
```

If you need to install it without github credentials, it is recomended to build the package file and include it within your project. You can customize the location of this file in your project. See 'How to modify the project' section on how to build the package files.

The below example references saving the file to a 'Packages' project subfolder. This would be the line you place in your requirements.txt.
```
./Packages/Logger-1.0.1.tar.gz
```

### Reference in your code:
Inside of your python files, at the top you can the following statements once. Typically  create_logger() should only be called once from your primary/main thread. 
```
import Logger
logging = Logger.create_logger()
```

Whenever you need to reference a new logger, you can use the following code. Typically this can be when you're starting a file, or defining a new class.
```
logger = logging.getLogger("Logger Name Goes Here")
```

You can then reference the logger object like you would normally do so with the default logging module in python. For example:
```
logger.debug('This is a debug message!')
logger.info("This is an info message!")
logger.warning('Uh oh, a warning!')
logger.error('Something bad happened, like an exception!')
```

A basic example of usage can be found in the 'Tests' subfolder of this project.

## How to modify the project
Follow this section if you are looking to make changes to the Logger class. It will guide you through setting up the development environment.

1. Clone the repository:
   ```git clone https://github.com/ULL-IR-Office/Logger.git```

2. Set up a Python virtual environment. For windows, there is a `Create Virtual Environment.bat` file within the `Setup` subfolder that will automatically set up the virtual environment and all dependencies.

3. Set up the default configurations. Run the `Create Configs.bat` file in the `Setup` folder. This will create a configs subfolder and configuration files for the logger. Alternatively, you can manually run the `Create Configs.py` file using the virual environment. A Logger.ini file will be generated in a `Configs` subfolder with instructions on how to modify it within the file.

4. The `Tests` subfolder contains an example usage of how to run the module while you modify it.

5. When you need to build the package, you can utilize the `Build Packages.bat` file in the `Setup` subfolder. It will drop the tar.gz and wheel file into a dist subfolder. Alternatively, you call the following two commands from the project directory. 
```
 py -m pip install --upgrade build
 py -m build
```
For non-windows development environments please reference python's documentation. `https://packaging.python.org/en/latest/tutorials/packaging-projects/`
