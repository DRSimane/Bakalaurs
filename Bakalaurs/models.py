
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
    source: str # mezgls, no kura sākas pāreja
    target: str #mezgls uz kuru pāriet
    condition: Optional[str] = None # nosacījums - valid/invalid

# aktivitāšu struktūra 
@dataclass
class ActivityDiagram:
    nodes: List[Node] #visu mezglu saraksts
    edges: List[Edge] #visi savienojumi