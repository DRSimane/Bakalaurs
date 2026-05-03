import xml.etree.ElementTree as ET
from models import Node, Edge, ActivityDiagram

def detect_node_type(value: str, style: str) -> str:
    #automatiska mezgla tipa noteiksana
    style = (style or "").lower()
    v = (value or "").lower()

    #start mezgls 
    if "startstate" in style:
        return "start"

    #end mezgls
    if "endstate" in style:
        return "end"
    
    if "perimeter=join" in style:
        return "join"
    
    if "perimeter=fork" in style:
        return "fork"

    # vai mezgla ir value
    if "error" in v:
        return "error"

    #izveles mezgli
    if "rhombus" in style or "diamond" in style:
        return "decision"

    return "action"

def load_diagram_from_drawio_xml(path: str) -> ActivityDiagram:
    tree = ET.parse(path)
    root = tree.getroot()

    nodes = []
    edges = []
    edge_labels = {}

    for cell in root.iter("mxCell"):
        cell_id = cell.get("id")
        value = cell.get("value") or ""
        style = cell.get("style") or ""
        vertex = cell.get("vertex")
        edge = cell.get("edge")
        parent = cell.get("parent")

        # nosacījumi
        if "edgeLabel" in style and parent:
            edge_labels[parent] = value.strip("[]{} ")
            continue

        # mezgli
        if vertex == "1" and "edgeLabel" not in style:
            node_type = detect_node_type(value, style)

            # nosaukt izveles mezglu
            if node_type == "decision" and value.strip() == "":
                value = "Izvēles mezgls"

            nodes.append(Node(cell_id, value, node_type))

        # parejas
        if edge == "1":
            source = cell.get("source")
            target = cell.get("target")
            edges.append(Edge(cell_id, source, target, None))

    # nosacijumi parejam
    for e in edges:
        if e.id in edge_labels:
            e.condition = edge_labels[e.id]

    return ActivityDiagram(nodes, edges)
    
