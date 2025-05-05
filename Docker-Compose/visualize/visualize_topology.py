import json
import os

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import Patch


def visualize_topology():
    with open('network_data.json', 'r') as f:
        data = json.load(f)
 
    devices = data['devices']
    links = data['links']
    port_channels = data.get('port_channels', {})
 
    role_layers = {"Core": 0, "Distribution": 1, "L2 Access": 2}
    role_icons = {"Core": "images/core.png", "Distribution": "images/distribution.png", "L2 Access": "images/l2_access.png"}
    role_colors = {"Core": "red", "Distribution": "orange", "L2 Access": "skyblue"}
 
    positions = {}
    node_roles = {}
    devices_by_role = {}
 
    for hostname, info in devices.items():
        role = info.get("role", "Unknown")
        node_roles[hostname] = role
        devices_by_role.setdefault(role, []).append(hostname)
 
    # Pyramid structure layout
    layer_order = ["Core", "Distribution", "L2 Access"]
    layer_heights = {role: -i for i, role in enumerate(layer_order)}
    max_width = max(len(devices_by_role.get(role, [])) for role in layer_order)
 
    for role in layer_order:
        hosts = sorted(devices_by_role.get(role, []))
        y = layer_heights[role]
        n = len(hosts)
        start_x = (max_width - n) / 2
        for i, hostname in enumerate(hosts):
            x = start_x + i
            positions[hostname] = (x, y)
 
    portchannel_interfaces = set()
    portchannel_connections = {}
 
    for pc_id, members in port_channels.items():
        devices_in_pc = [pc['device'] for pc in members]
        if len(devices_in_pc) == 2:
            dev1, dev2 = devices_in_pc
            key = tuple(sorted([dev1, dev2]))
            portchannel_connections[key] = pc_id
        for pc in members:
            device = pc["device"]
            for iface in pc["interfaces"]:
                portchannel_interfaces.add((device, iface))
 
    G = nx.DiGraph()
    for hostname in devices:
        G.add_node(hostname)
 
    for link in links:
        src, src_port, dst, dst_port = link
        if (src, src_port) in portchannel_interfaces or (dst, dst_port) in portchannel_interfaces:
            continue
        label = f"{src_port} — {dst_port}"  # Changed label format
        G.add_edge(src, dst, label=label)
 
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_title("Network Architecture Based on Input", fontsize=16)
    ax.set_axis_off()
 
    nx.draw_networkx_edges(G, pos=positions, ax=ax, edge_color='gray', arrows=True)
 
    # Annotate source and destination port labels separately
    for (src, dst, data) in G.edges(data=True):
        src_port, dst_port = data['label'].split(' — ')  # Split our custom label
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
    
        # Source port label (slightly toward the destination)
        ax.text(
            x1 + (x2 - x1) * 0.20,
            y1 + (y2 - y1) * 0.20,
            src_port,
            fontsize=9,
            ha='center',
            va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2')
        )
    
        # Destination port label (slightly toward the source)
        ax.text(
            x2 + (x1 - x2) * 0.20,
            y2 + (y1 - y2) * 0.20,
            dst_port,
            fontsize=9,
            ha='center',
            va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2')
        )
 
    for hostname in G.nodes:
        role = node_roles.get(hostname, "Unknown")
        img_path = role_icons.get(role)
        if img_path and os.path.exists(img_path):
            image = plt.imread(img_path)
            im = OffsetImage(image, zoom=0.75)
            ab = AnnotationBbox(im, positions[hostname], frameon=False)
            ax.add_artist(ab)
        else:
            ax.text(*positions[hostname], hostname, ha='center', va='center',
                    bbox=dict(facecolor=role_colors.get(role, 'gray'), boxstyle='round,pad=0.3'))
 
    for hostname in G.nodes:
        x, y = positions[hostname]
        label = hostname
        ax.text(x, y + 0.12, label, ha='center', va='center', fontsize=13, color='black')
 
    visited = set()
    for (dev1, dev2), pc_id in portchannel_connections.items():
        if (dev1, dev2) in visited or (dev2, dev1) in visited:
            continue
        visited.add((dev1, dev2))
 
        x1, y1 = positions[dev1]
        x2, y2 = positions[dev2]
        ax.annotate("", xy=(x2 - 0.085, y2), xytext=(x1 + 0.085, y1),
                    arrowprops=dict(arrowstyle="<->", color='blue', lw=2.5, linestyle='dashed'))

        interfaces = []
        for pc in port_channels[str(pc_id)]:
            if pc['device'] == dev1 or pc['device'] == dev2:
                interfaces.extend(pc['interfaces'])

        label = f"Port-Channel {pc_id}:\n {', '.join(interfaces)}"
        # Adjust label position
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 0.05
        ax.text(mid_x, mid_y, label, fontsize=9, color='blue', ha='center', va='center')
 
    # legend_elements = [
    #     Patch(facecolor='red', label='Core'),
    #     Patch(facecolor='orange', label='Distribution'),
    #     Patch(facecolor='skyblue', label='L2 Access')
    # ]
    # ax.legend(handles=legend_elements, loc='lower left')
 
    plt.tight_layout()
    plt.savefig("architecture_Image/network_topology.png", dpi=300)
   # nx.write_graphml(G, "network_topology.graphml")
    plt.show()