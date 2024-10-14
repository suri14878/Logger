# Logger Package

## Introduction
This project wraps the default python logging library to make it easier to work with and standarizes output options for internal projects.

## How to use the project
Follow this section if you are looking to user the Logger class in other projects.

## How to modify the project
Follow this section if you are looking to make changes to the Logger class. It will guide you through setting up the development environment.

1. Clone the repository:
   ```git clone https://github.com/ULL-IR-Office/Logger.git```

2. Set up a Python virtual environment. For windows, there is a `Create Virtual Environment.bat` file within the `Setup` subfolder that will automatically set up the virtual environment and all dependencies.

3. Set up the default configurations. Run the `Create Configs.bat` file in the `Setup` folder. This will create a configs subfolder and configuration files for the logger. Alternatively, you can manually run the `Create Configs.py` file using the virual environment. A Logger.ini file will be generated in a `Configs` subfolder with instructions on how to modify it within the file.

4. The `Tests` subfolder contains an example usage of how to run the module while you modify it.

5. When you're ready to build the package, you can utilize the `Build Packages.bat` file in the `Setup` subfolder. Alternatively, you call the following two commands from the project directory. 
```
 py -m pip install --upgrade build
 py -m build
```
For non-windows development environments please reference python's documentation. `https://packaging.python.org/en/latest/tutorials/packaging-projects/`
