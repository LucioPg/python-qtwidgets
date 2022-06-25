import subprocess
import os
from qtwidgets.configuration.config import Configuration
from qtwidgets.configuration.constants import config_designer_path, plugin_folder

def start():
    config = Configuration(config_designer_path)
    if config.use_custom_path:
        PYQTDESIGNERPATH = config.paths.pyqtdesignerpath.replace('|', ';') # maybe is not possible to chain paths
    else:
        PYQTDESIGNERPATH = plugin_folder

    os.environ['PYQTDESIGNERPATH'] = PYQTDESIGNERPATH


    p = subprocess.Popen(f"{config.executable.bin} {config.executable.argument}", stdout=subprocess.PIPE, shell=True).stdout.read()

