import sys
import os

MAJOR_VERSION_INDEX = 0
PYTHON_VERSION = 3

WINDOWS = "win32"
OSX = "darwin"
LINUX = "linux"

WINDOWS_PYTHON = "python"
OSX_PYTHON = "python3"
LINUX_PYTHON = "python3"
GENERIC_PYTHON = ""

this_operating_system = ""

# Size of the following arrays must match
list_of_libraries = ["Flask", "numpy", "SQLAlchemy", "flask-wtf", "faker", "pytest", "requests"]
version_of_libraries = ["1.0.2", "1.15.1", "1.2.11", "0.14.2", "0.9.1", "3.9.1", "2.20.0"]

# Make sure python3.X is running
if not (sys.version_info[MAJOR_VERSION_INDEX] == PYTHON_VERSION):
    print("Not running python 3!")
    sys.exit(0)

# Compensate for OS
this_operating_system = sys.platform.lower()

if this_operating_system == WINDOWS:
    GENERIC_PYTHON = WINDOWS_PYTHON

elif this_operating_system == OSX:
    GENERIC_PYTHON = OSX_PYTHON

elif this_operating_system == LINUX:
    GENERIC_PYTHON = LINUX_PYTHON

else:
    print("Not on windows, osx or linux!")
    sys.exit(0)

# Upgrade pip
os.system(GENERIC_PYTHON + " -m pip install --upgrade pip")

# Install libraries with correct version
for library, version in zip(list_of_libraries, version_of_libraries):
    os.system(GENERIC_PYTHON + " -m pip install " + library + "==" + version)

print("\nPackages installed successfully.")
