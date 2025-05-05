import json

import requests
from parse_device.parse_device import parse_devices
from visualize.visualize_topology import visualize_topology


def main():
    api_url = "https://35xdq8xs-8000.inc1.devtunnels.ms/api/netgenie/finalPush/filecreation/search?groupName=Site 1_Corporate Office_Cisco_CAT9K_3Tier_001"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        json_input = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON received from API.")
        return

    devices, links, port_channels = parse_devices(json_input)
    device_dict = {
        device['hostname']: {
            'ip': device['ip'],
            'role': device['role']
        }
        for device in devices
    }

    links_list = [
        [link['source'], link['source_port'], link['target'], link['target_port']]
        for link in links
    ]

    port_channel_dict = {}
    for hostname, pcs in port_channels.items():
        for pc_id, interfaces in pcs.items():
            if pc_id not in port_channel_dict:
                port_channel_dict[pc_id] = []
            port_channel_dict[pc_id].append({
                "device": hostname,
                "interfaces": interfaces
            })

    output_data = {
        "devices": device_dict,
        "links": links_list,
        "port_channels": port_channel_dict
    }

    with open("network_data.json", "w") as f:
        json.dump(output_data, f, indent=4)

    visualize_topology()

if __name__ == "__main__":
    main()
