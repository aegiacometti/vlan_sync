import os
from etc import ops


class Inventory:
    """
    Load Inventory from different sources (check vlan_sync_cfg.yml)
    """
    def __init__(self, sources, logger):
        self.sources = sources
        self.devices = self.load_inventory()
        self.logger = logger
        self.userid = os.getenv("USERNAME")
        self.passwd = os.getenv("PASSWORD")

    def __repr__(self):
        return f"<Inventory(Sources={self.sources}, Devices={self.devices}>"

    def load_inventory(self):
        inv = {}
        for source in self.sources:
            inv = self.get_source(source)
        return inv

    def get_source(self, source_type):
        devices_full_list = []
        if source_type == "remote_api_urls":
            # NOT implemented yet
            pass
        elif source_type == "file_list":
            for item in self.sources[source_type]:
                devices = ops.load_yaml(item["filename"])
                if len(devices) != 0:
                    devices_full_list.extend(self.add_devices_per_source(devices))
        else:
            self.logger.info(f"SKIPPING Not valid inventory source {source_type}")

        return devices_full_list

    def add_devices_per_source(self, devices):
        device_list_per_source = []
        for device in devices["hosts"]:
            if self.validate_device(device):
                device["username"] = self.userid
                device["password"] = self.passwd
                device_list_per_source.append(device)
            else:
                self.logger.info(f"SKIPPING Invalid device {device}")

        return device_list_per_source

    def validate_device(self, device):
        # Not implemented yet. Check duplicate, host, ip address, and device type
        return device









