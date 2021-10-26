import re
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


def run_cmd(device: dict, command: str, logger_poller) -> list:
    """
    Get device output according to the command
    :param device: device info
    :param command: to execute on device
    :param logger_poller: logging object
    :return: parsed response in dictionary format
    """
    name = device.pop("name")
    try:
        with ConnectHandler(**device) as conn:
            # When pyATS and Genie installed add use_genie=True
            response = conn.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logger_poller.error(e)
        logger_poller.error(f"Connection error to device {device}")
        return []
    device['name'] = name
    # When pyATS and Genie installed change return to response
    parsed = custom_parser(response, command, device['device_type'], logger_poller)
    logger_poller.info(f"Device {device} - Vlans Parsed")
    logger_poller.debug(f"{parsed}")
    return parsed
    # return response


def custom_parser(output: str, command: str, device_type: str, logger_poller) -> list:
    # Install pip install pyATS and genie to use the parser in Netmiko. Now is not necessary for 1 command to parse
    """
    Command output parse to structured data
    :param output: string
    :param command: executed command
    :param device_type: device type supported by Netmiko
    :param logger_poller: logging object
    :return:
    """
    parsed_output = []
    if command == "show vlan" and device_type == "cisco_ios":
        output = output.split("\n")
        pattern = r"^(\d+)\s+(\S+)\s+\S+.*$"
        for line in output:
            match = re.search(pattern, line)
            if match:
                parsed_output.append({"vlan_id": match.group(1), "vlan_name": match.group(2)})
    else:
        logger_poller.info(f"Parsed not implemented for command {command} on device_type {device_type}")
    return parsed_output


# ar-mun-cd-11-dc-01#show vlan
#
# VLAN Name                             Status    Ports
# ---- -------------------------------- --------- -------------------------------
# 1    default                          active    Gi0/3, Gi0/4, Gi0/5, Gi0/6, Gi0/7, Gi0/8, Gi0/9, Gi0/10, Gi0/11, Gi0/12, Gi0/13, Gi0/14, Gi0/15, Gi1/1, Gi1/3
# 101  Munro-SRV33A                     active
# 117  Munro-USER33.128                 active
# 118  gestion_IA                       active
# 119  Munro-ELAN                       active
# 121  Munro-SEG64A                     active    Gi0/16, Gi0/17, Gi0/18, Gi0/19, Gi0/20, Gi0/21, Gi0/22, Gi0/23, Gi0/24
# 138  VL138-172.21.66.0/26-Seguridad   active
# 840  VOIP-SSMR                        active
# 999  dump-vlan                        active
# 1002 fddi-default                     act/unsup
# 1003 token-ring-default               act/unsup
# 1004 fddinet-default                  act/unsup
# 1005 trnet-default                    act/unsup
#
# VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
# ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
# 1    enet  100001     1500  -      -      -        -    -        0      0
# 101  enet  100101     1500  -      -      -        -    -        0      0
# 117  enet  100117     1500  -      -      -        -    -        0      0
# 118  enet  100118     1500  -      -      -        -    -        0      0
# 119  enet  100119     1500  -      -      -        -    -        0      0
# 121  enet  100121     1500  -      -      -        -    -        0      0
# 138  enet  100138     1500  -      -      -        -    -        0      0
# 840  enet  100840     1500  -      -      -        -    -        0      0
# 999  enet  100999     1500  -      -      -        -    -        0      0
# 1002 fddi  101002     1500  -      -      -        -    -        0      0
# 1003 tr    101003     1500  -      -      -        -    -        0      0
# 1004 fdnet 101004     1500  -      -      -        ieee -        0      0
# 1005 trnet 101005     1500  -      -      -        ibm  -        0      0
#
# Remote SPAN VLANs
# ------------------------------------------------------------------------------
#
#
# Primary Secondary Type              Ports
# ------- --------- ----------------- ------------------------------------------
#
# ar-mun-cd-11-dc-01#