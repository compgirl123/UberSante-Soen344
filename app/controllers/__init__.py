from app.common_definitions.common_paths import PATH_TO_CONTROLLERS
import glob
import os

__all__ =  [os.path.basename(f).replace(".py","") for f in glob.glob(PATH_TO_CONTROLLERS + "/" + "*Controller.py")]
