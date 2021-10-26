from etc import ops
import sys


def get_config(cfg_file) -> dict:
    """
    Get tool configuration
    :param cfg_file: Configuration filename
    :return: config dict
    """
    cfg = ops.load_yaml(cfg_file)
    if len(cfg.get('inventory_sources', '')) == 0:
        print("No inventory sources detected")
        sys.exit(1)

    return cfg
