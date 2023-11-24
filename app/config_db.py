import os
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

dir_path = os.path.dirname(os.path.realpath(__file__))  # url of project
root_dir = dir_path[:-3]  # file venv - env - db
config = Config(f'{root_dir}.env')

database_url = f'sqlite:///{root_dir}' + config('db_name', cast=str)

SECRET_KEY = config('SECRET_KEY', cast=Secret)
