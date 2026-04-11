
# dataclass dekorators, lai viegli definētu datu struktūras
from dataclasses import dataclass
#tipēšanas rīki
from typing import List, Optional

# klase aktivitāšu diagrammas mezglam
@dataclass 
class Node: 
    id: str # identifikators
    label: str # diagrammas teksts
    type: str # start, action, decision, end - mezgla tips

# savienojums starp mezgliem
@dataclass
class Edge: 
    def __init__(self, id, source, target, condition):
        self.id = id
        self.source = source
        self.target = target
        self.condition = condition

# aktivitāšu struktūra 
@dataclass
class ActivityDiagram:
    nodes: List[Node] #visu mezglu saraksts
    edges: List[Edge] #visi savienojumi

    def explain_edges_readable(self):
        node_map = {n.id: n.label or "(tukšs)" for n in self.nodes}
        explanations = []
        seen = set()

        for e in self.edges:
            if e.source == e.target: #tiek izlaists self-loop
                continue

            source_name = node_map.get(e.source, e.source)
            target_name = node_map.get(e.target, e.target)

            if source_name.strip() == "" and target_name.strip() == "":
                continue

            key = (source_name, target_name, e.condition)
            if key in seen:
                continue
            seen.add(key)

            if e.condition:
                explanations.append(
                    f"Ja nosacījums {e.condition} ir patiess, tad no mezgla '{source_name}' pāreja ved uz mezglu '{target_name}'."
                )
            else:
                explanations.append(
                    f"No mezgla '{source_name}' pāreja ved uz mezglu '{target_name}'."
                )
        return explanations
    def get_edge_expl(self):
        return self.explain_edges_readable()