__all__ = [
    'Configuration'
]
from configparser import ConfigParser, SectionProxy
import os
import logging
logger = logging.getLogger(__name__)
try:

    from qtwidgets.configuration.constants import config_designer_path
except ImportError as err:
    print(err)

    from qtwidgets.configuration.constants import config_designer_path
_CONFIGURATION_PATH = config_designer_path # os.path.join(os.path.dirname(__file__), config_designer_path)


class Configuration:
    """ This class allows to load a configuration file as ini format and automatically
     generate attributes for the class based on the sections and their values, for example:
     >>>conf = Configuration()
     >>>conf._login.username
     >>> test_user"""
    def __init__(self, other_config_path=None):
        self._config = self.__init_reader(other_config_path)
        self.__recursive_read(self._config)


    def __init_reader(self, other_config_path):
        config = ConfigParser()
        config_path = _CONFIGURATION_PATH if other_config_path is None else other_config_path
        if not os.path.exists(config_path):
            logger.critical(f'The configuration file name {config_path} does not exist')
            raise Exception(f'The configuration file name {config_path} does not exist')
        config.read(config_path)
        return config

    def __recursive_read(self, config_dict: dict):
        def inner(cls, dict_obj):
            for key, val in dict_obj.items():
                is_section = isinstance(val, SectionProxy)
                if not is_section and val.lower() in ['true', 'false', 'none', None]:
                    val = True if val.lower() == 'true' else False
                setattr(cls, key.lower(), val)
                if is_section:
                    inner(getattr(cls, key.lower()), val)
        return inner(self, config_dict)

    def sections(self):
        return self._config.sections()

    def options(self, section):
        opt, val = None, None
        if section.upper() in self._config:
            return {opt: value for opt, value in self._config[section.upper()].items()}
        else:
            logger.warning(f'the section "{section}" could not exist')
            return opt, val


if __name__ == '__main__':
    a = Configuration()
    a.test
    print