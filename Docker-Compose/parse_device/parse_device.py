from collections import defaultdict


def parse_devices(json_data):
    devices = []
    links = []
    port_channels = defaultdict(lambda: defaultdict(list))  # {hostname: {pc_id: [interfaces]}}

    for device_entry in json_data:
        for ip, config_list in device_entry.items():
            device_info = {"ip": ip, "interfaces": [], "hostname": "", "role": ""}

            # Extract hostname and role
            for section in config_list:
                if "location" in section:
                    loc = section["location"][0]
                    device_info["hostname"] = loc["hostname"]
                    device_info["role"] = loc["switchRole"]
                    break

            # Extract interfaces and neighbors
            for section in config_list:
                if "interface" in section:
                    for intf in section["interface"]:
                        device_info["interfaces"].append(intf)

                        pc_id = intf.get("portChannelId")
                        if pc_id and pc_id != 1:
                            port_channels[device_info["hostname"]][pc_id].append(intf["interface"])

                        if "neighborHostname" in intf and intf["neighborHostname"]:
                            neighbor = {
                                "source": intf["hostname"],
                                "source_port": intf["interface"],
                                "target": intf["neighborHostname"],
                                "target_port": intf["neighborPort"]
                            }
                            links.append(neighbor)

            devices.append(device_info)

    return devices, links, port_channels