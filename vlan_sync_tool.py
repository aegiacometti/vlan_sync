#!/usr/bin/env python

import argparse
import asyncio
import logging
import concurrent.futures

from etc.config import get_config
from etc.inventory import Inventory
from etc.db_ops import init_db, query_all_vlan
from etc.device_ops import run_cmd
from etc.logger_svc import CustomLogger
from etc.updater import update_vlans

DEFAULT_CONFIG_FILE = "vlan_sync_cfg.yml"
DEFAULT_INVENTORY_FILE = "inventory.yml"


def get_device_vlans(device, command, logger_poller):
    """
    Get device VLANs
    """
    vlans_device = run_cmd(device, command, logger_poller)

    """
    testing data
    vlans_device = [{'vlan_id': '1', 'vlan_name': 'default'}, {'vlan_id': '110', 'vlan_name': 'vlan'},
                    {'vlan_id': '200', 'vlan_name': 'INET_DTV'}, {'vlan_id': '201', 'vlan_name': 'para_borrar'},
                    {'vlan_id': '202', 'vlan_name': 'Internet_Broadband'},
                    {'vlan_id': '251', 'vlan_name': 'InsideFW_REGION(172.21.0.160/29)'},
                    {'vlan_id': '280', 'vlan_name': 'INSIDE_CONC_VPN(172.21.1.0/28)'},
                    {'vlan_id': '302', 'vlan_name': 'MPLS-IN'}, {'vlan_id': '303', 'vlan_name': 'descri'},
                    {'vlan_id': '304', 'vlan_name': 'OutLevel3(201.234.41.80/28)'},
                    {'vlan_id': '308', 'vlan_name': 'WIFI-PROV-OUT'},
                    {'vlan_id': '400', 'vlan_name': 'MGMT(172.21.31.32/29)'},
                    {'vlan_id': '401', 'vlan_name': 'WLC-MGMT(172.21.31.0/29)'},
                    {'vlan_id': '402', 'vlan_name': 'ARG2FW(172.21.31.16/29)'},
                    {'vlan_id': '404', 'vlan_name': 'WLC-corp(172.21.92.0/22)'},
                    {'vlan_id': '405', 'vlan_name': 'WLC-Guest'}, {'vlan_id': '406', 'vlan_name': 'WIFI-Prov'},
                    {'vlan_id': '407', 'vlan_name': 'ISE(172.21.31.40/29)'}, {'vlan_id': '408', 'vlan_name': 'WLC-HA'},
                    {'vlan_id': '440', 'vlan_name': 'Failover-FW-AR-MTZ-FW-01-Guest'},
                    {'vlan_id': '441', 'vlan_name': 'Failover-FW-AR-MTZ-VC-01'},
                    {'vlan_id': '442', 'vlan_name': 'Failover-FW-AR-MTZ-CO-01'},
                    {'vlan_id': '443', 'vlan_name': 'Failover-FW-AR-MTZ-FW-01-Prov'},
                    {'vlan_id': '445', 'vlan_name': 'Failover-Fw-DTV-FW-DC-C-1'},
                    {'vlan_id': '950', 'vlan_name': 'BC-AFM(172.21.1.16/28)'},
                    {'vlan_id': '999', 'vlan_name': 'dump-vlan'},
                    {'vlan_id': '1002', 'vlan_name': 'fddi-default'},
                    {'vlan_id': '1003', 'vlan_name': 'token-ring-default'},
                    {'vlan_id': '1004', 'vlan_name': 'fddinet-default'},
                    {'vlan_id': '1005', 'vlan_name': 'trnet-default'},
                    {'vlan_id': '1', 'vlan_name': 'enet'}, {'vlan_id': '110', 'vlan_name': 'enet'},
                    {'vlan_id': '200', 'vlan_name': 'enet'}, {'vlan_id': '201', 'vlan_name': 'enet'},
                    {'vlan_id': '202', 'vlan_name': 'enet'}, {'vlan_id': '251', 'vlan_name': 'enet'},
                    {'vlan_id': '280', 'vlan_name': 'enet'}, {'vlan_id': '302', 'vlan_name': 'enet'},
                    {'vlan_id': '303', 'vlan_name': 'enet'}, {'vlan_id': '304', 'vlan_name': 'enet'},
                    {'vlan_id': '308', 'vlan_name': 'enet'}, {'vlan_id': '400', 'vlan_name': 'enet'},
                    {'vlan_id': '401', 'vlan_name': 'enet'}, {'vlan_id': '402', 'vlan_name': 'enet'},
                    {'vlan_id': '404', 'vlan_name': 'enet'}, {'vlan_id': '405', 'vlan_name': 'enet'},
                    {'vlan_id': '406', 'vlan_name': 'enet'}, {'vlan_id': '407', 'vlan_name': 'enet'},
                    {'vlan_id': '408', 'vlan_name': 'enet'}, {'vlan_id': '440', 'vlan_name': 'enet'},
                    {'vlan_id': '441', 'vlan_name': 'enet'}, {'vlan_id': '442', 'vlan_name': 'enet'},
                    {'vlan_id': '443', 'vlan_name': 'enet'}, {'vlan_id': '445', 'vlan_name': 'enet'},
                    {'vlan_id': '950', 'vlan_name': 'enet'}, {'vlan_id': '999', 'vlan_name': 'enet'},
                    {'vlan_id': '1002', 'vlan_name': 'fddi'}, {'vlan_id': '1003', 'vlan_name': 'tr'},
                    {'vlan_id': '1004', 'vlan_name': 'fdnet'}, {'vlan_id': '1005', 'vlan_name': 'trnet'}]
    """

    if len(vlans_device) == 0:
        logger_poller.info(f"Vlan list is empty. Check host {device.name}or db.\n"
                           f"Host {device.name}\n")
        return
    vlans_device_to_list = [[k, v] for x in vlans_device for k, v in x.items()]
    return vlans_device_to_list


def vlans_difference(vlans_db, vlans_device, logger_poller):
    """
    Check differences and return a dict with them
    """
    # TODO check for differences.
    difference = [{"device": True, "dev_name": "xxx",
                   "operation_type": "add/remove/update",
                   "vlan_id": "1", "vlan_name": "name"},
                  {"device": False, "dev_name": "database",
                   "operation_type": "add/remove/update",
                   "vlan_id": "1", "vlan_name": "name",
                   "vlan_description": "change_me"}]
    logger_poller.debug(f"VLANs to sync {difference}")
    return difference


def sync_device(vlans_db, device, command, logger_poller, logger_orm):
    """
    Get device VLANs and check if they are the same
    """
    vlans_device = get_device_vlans(device, command, logger_poller)
    vlans_difference_result = vlans_difference(vlans_db, vlans_device, logger_poller)
    if len(vlans_difference_result) != 0:
        update_vlans(vlans_difference_result, logger_poller, logger_orm)
        logger_poller.info(f"Device {device} updated")
    else:
        logger_poller.info(f"Device {device} in sync")


async def sync_vlans(executor, inventory, session_obj, logger_poller, logger_orm):
    """
    Get VLANs from DB and pool devices with threads
    """
    loop = asyncio.get_event_loop()
    command = "show vlan"
    tasks = []
    logger_orm.info("Getting VLANs from DB")
    vlans_db = query_all_vlan(session_obj, logger_orm)
    logger_poller.info("Staring the poller")
    for device in inventory:
        tasks.append(loop.run_in_executor(executor, sync_device, vlans_db, device, command, logger_poller, logger_orm))
    completed, pending = await asyncio.wait(tasks)
    # results = [t.result() for t in completed]
    logger_poller.info(f"Sync finished")


def main(args):
    """
    Tool to sync VLAN between between devices and DB (ORM)
    :param args: optional: file, polling time, inventory (check vlan_sync_cfg.yml)
    """
    config = get_config(args.file) if args.file else get_config(DEFAULT_CONFIG_FILE)
    logging.basicConfig(level=logging.DEBUG)
    logger_poller = CustomLogger("main", config["poller"])
    logger_orm = CustomLogger("sqlalchemy", config["db_orm"])
    inventory = Inventory(config.get('inventory_sources', ''), logger_poller)
    session_obj = init_db()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=config["poller"].get("workers", 4))
    # Will have asyncio ready for other tasks, but the polling is with thread workers for 2 reasons:
    # - Netmiko and SQLAlchemy are NOT Asyncio ready
    # - Polling too many devices could DoS authentication systems, overload the network or this same PC
    # Later could use asyncio semaphore to limit the polled devices if changing library to "netdev",
    # which is a port of asyncio version of Netmiko. But currently does not have all the extensions.
    # Scrapli is another good option, but I had problems in my Lab device which doesn't make any sense to work on now.
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(sync_vlans(executor, inventory.devices, session_obj, logger_poller, logger_orm))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Multi-vendor VLAN sync tool")
    parser.add_argument("-f", "--file", help="Main tool configuration filename (for testing purposes")
    parser.add_argument("-p", "--polling_time", help="Main tool configuration filename (for testing purposes)")
    parser.add_argument("-i", "--inventory", help="Fixed inventory file name (for testing purposes)")
    options = parser.parse_args()
    main(options)
