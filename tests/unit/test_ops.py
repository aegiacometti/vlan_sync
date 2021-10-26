import etc.ops

valid_filename = "mock_data/vlan_sync_cfg.yml"
invalid_file = "mock_data/dummy.txt"


def test_file_found():
    assert etc.ops.load_yaml(valid_filename)


def test_file_not_found():
    assert not etc.ops.load_yaml("")


def test_valid_yml_file():
    assert etc.ops.load_yaml(valid_filename)


def test_invalid_yml_file():
    assert not etc.ops.load_yaml(invalid_file)
