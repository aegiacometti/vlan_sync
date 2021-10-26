import yaml
import sys


def load_yaml(filename) -> dict:
    """
    Common load YML file
    :param filename: filename
    :return: file dict
    """
    content = {}
    try:
        with open(filename) as file:
            content = yaml.safe_load(file.read())
    except Exception as e:
        print(e)
        print(f"Error loading file {filename}")

    if isinstance(content, dict):
        return content
    else:
        print(f"{filename} is not a valid YAML file")
        return {}


load_yaml("../vlan_sync_cfg.yml")