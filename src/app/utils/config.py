"""Centralized loading and parsing of configuration files, and provide a unified access interface.
Singleton pattern: ensure configuration consistency.
"""

import datetime
from pathlib import Path

import numpy as np
from pydantic import BaseModel, ConfigDict

from .file_io import check_path, read_toml, save_toml

__all__ = ['CONF', 'PathData', 'load_config', 'save_config']


current_time = datetime.datetime.now()

script_path = Path(__file__).resolve()
parts = script_path.parts
src_index = parts.index('src')  # get the index of "src"
root_path = Path(*parts[:src_index])  # get all parts before "src"


class PathData:
    """Naming conventions and path-related attributes.

    - xx_name
        - folder name without trailing '/'
        - file name with extension
    - xx_name_base
        - file name without extension
    - xx_path
        - folder relative path with '/'
        - file relative path with extension
    - xx_path_abs
        - file absolute path
    """

    root_path_abs: Path = root_path
    usr_local_path: Path = Path('usr/local/')
    usr_default_path: Path = Path('usr/default/')
    usr_lib_path: Path = Path('usr/lib/')
    default_empty_file_path: Path = usr_default_path / 'empty.toml'

    config_file_path: Path = usr_local_path / 'config.toml'
    default_config_file_path: Path = usr_default_path / 'default.config.toml'

    """
    Log files
    """
    filename_base_current_time_sec: str = current_time.strftime(r'%H-%M-%S')
    filename_base_current_time_min: str = current_time.strftime(r'%H-%M')
    filename_base_current_time_hour: str = current_time.strftime(r'%H')
    filename_base_current_time_day: str = current_time.strftime(r'%Y-%m-%d')
    log_filename: str = f'{filename_base_current_time_hour}.log'
    log_folder_name: str = filename_base_current_time_day
    log_folder_parent_path: Path = Path('output/logs/')
    log_folder_path: Path = log_folder_parent_path / log_folder_name
    case_workdir_path: Path = log_folder_path
    report_folder_path: Path = Path('output/reports/')

    """
    Figures
    """
    default_fig_name: str = f'{filename_base_current_time_sec}.png'
    default_fig_path: Path = log_folder_path / default_fig_name


# Create temporary folders and files
for dir_path in [PathData.log_folder_path, PathData.report_folder_path]:
    check_path(target_path=dir_path, is_dir=True)

for target_path, default_path in [
    (PathData.config_file_path, PathData.default_config_file_path),
]:
    check_path(target_path=target_path, default_path=default_path)


pydantic_config_dict = ConfigDict(
    str_to_lower=True,
    strict=True,
    extra='forbid',
    arbitrary_types_allowed=True,
)


class ModifiedBaseModel(BaseModel):
    """BaseModel serialization of numpy.array to list."""

    model_config = pydantic_config_dict

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Convert numpy.array to list
        for k, v in data.items():
            if isinstance(v, np.ndarray):
                data[k] = v.tolist()
        return data


class Core(ModifiedBaseModel): ...


class Utils(ModifiedBaseModel):
    r"""Attributes:
    log_file_format(str): Log file format.
        Use double quotes, supports "\n" and "\t".
        Refer to the standard library logging/__init__.py: Formatter
    log_console_format(str): Console log format
    log_app_format(str): Application log format
    log_date_format(str): Date format.
        A wrong format may cause an infinite loop!!!
        ```python
        ...\\Lib\\logging\\__init__.py", line 650, in formatTime
            s = time.strftime(datefmt, ct)
        ValueError: Invalid format string
        ```
    text_editor_command(str): Text editor command.
    """

    # logs
    log_file_format: str = '%(asctime)s %(levelname)s %(message)s \tlocation: %(filename)s line%(lineno)d'
    log_console_format: str = '%(message)s %(asctime)s'
    log_app_format: str = '%(levelname)s %(message)s %(asctime)s'
    log_date_format: str = '%m/%d/%Y %H:%M:%S'
    text_editor_command: str = 'notepad.exe'


class Config(ModifiedBaseModel):
    """Global configuration file."""

    core: Core
    utils: Utils


def load_config(config_file_path: Path = PathData.config_file_path) -> Config:
    """Args:
        config_file_path(Path): Path to the configuration file
    Returns:
        Config: Parsed configuration object
    Raises:
        ValidationError: If parsing the configuration fails.
    """
    config_data = read_toml(config_file_path)
    return Config.model_validate(config_data)


def save_config(config: Config, config_file_path: Path | None = None) -> None:
    """Args:
    config(Config): Configuration object
    config_file_path(Path): Path to save the configuration file.
    """
    if config_file_path is None:
        check_path(PathData.config_file_path, PathData.default_config_file_path)
        config_file_path = PathData.config_file_path

    dict_data = config.model_dump(exclude_defaults=True)
    save_toml(file_path=config_file_path, dict_data=dict_data)


CONF = load_config()
