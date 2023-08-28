import os
import configparser


def cwd():
    return os.path.abspath('.')


def join_to_project_folder(relative_path: str):
    return os.path.join(cwd(), relative_path)


def read_config(path="productionentry/config.ini"):
    config = configparser.ConfigParser()
    full_path = join_to_project_folder(path)
    config.read(full_path)
    return config
