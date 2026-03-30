import xml.etree.ElementTree as ET
from models import Node, Edge, ActivityDiagram
import html

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

    # vai mezgla ir value
    if "error" in v:
        return "error"

    #izveles mezgli
    if "?" in v or "if" in v:
        return "decision"

    #sucess mezgli
    if "success" in v:
        return "action"

    return "action"


def load_diagram_from_drawio_xml(path: str) -> ActivityDiagram:
    tree = ET.parse(path)
    root = tree.getroot()

    mxgraph = root.find(".//mxGraphModel")
    if mxgraph is None:
        raise ValueError("Nav atrasts <mxGraphModel> XML failā.")

    mxroot = mxgraph.find("root")
    if mxroot is None:
        raise ValueError("Nav atrasts <root> iekš <mxGraphModel>.")

    nodes = []
    edges = []

    for cell in mxroot.findall("mxCell"):
        cell_id = cell.get("id")
        value = cell.get("value")
        vertex = cell.get("vertex")

        if value:
            value = html.unescape(value).strip()

        #Tikai vertex mezgli
        if vertex == "1":
            value = value or ""
            style = cell.get("style", "")
            node_type = detect_node_type(value, style)
            nodes.append(Node(cell_id, value, node_type))

	
    for cell in mxroot.findall("mxCell"):
        if cell.get("edge") != "1":
            continue

        source = cell.get("source")
        target = cell.get("target")

        # Ja source/target nav, mēģinām atrast mxPoint
        if not source or not target:
            geom = cell.find("mxGeometry")
            if geom is not None:
                source = source or geom.get("source")
                target = target or geom.get("target")

        # Ja joprojām nav - ignorējam malu
        if not source or not target:
            continue

        # Mala tiek saglabāta tikai, ja abi mezgli eksistē
        if not any(n.id == source for n in nodes):
            continue
        if not any(n.id == target for n in nodes):
            continue

        value = cell.get("value")
        if value:
            value = html.unescape(value).strip()

        edges.append(Edge(source, target, value))

    return ActivityDiagram(nodes, edges)
