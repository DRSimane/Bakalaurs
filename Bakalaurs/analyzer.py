
# Diagrammas modeļa imports
from models import ActivityDiagram

#Klase, kas veic UX analīzi 
class UXAnalyzer:

    #Konstruktors saņem diagrammu
    def __init__(self, diagram: ActivityDiagram):
        self.diagram = diagram # saglaba diagrammu ieksejai lietosanai

    #Funkcija, kas pārbauda vai pastāv mezgls uz sevi
    def detect_self_loops(self):
        loops = [] #saraksts atrastajiem cikliem

        #iteracija caur visam parejam
        for edge in self.diagram.edges:

            #ja pārejas sakuma un beigu mezgls sakrīt 
            if edge.source == edge.target:
                loops.append(edge) #saglaba ka problemu 

        return loops #Atgriež atrastos ciklus 

        #funkcija, kas pārbauda vai pastāv potenciāli bezgalīgi retry cikli
    def detect_retry_cycles(self):

            problems = [] #saraksts problēmām

            # visu pāreju pārbaude
            for edge in self.diagram.edges:
                #ja nosacījums retry
                if edge.condition == "retry":
                    problems.append(
                        "Iespējams bezgalīgs retry loop."
                    )
            return problems
        
    #funkcija, kas pārbauda vai ir nepieejami mezgli 
    def detect_unreachable_nodes(self):

        #saglabā mezglus, kuri ir sasniedzami
        reachable = set() 

        #atrod sākuma mezglu
        start_nodes = [n for n in self.diagram.nodes if n.type == "start"]

        #ja nav start mezgla
        if not start_nodes:
            return ["Netika atrasts start mezgls."]

        #sakuma mezgls
        start_id = start_nodes[0].id

        #rekursīva dfs funkcija
        def dfs(node_id):
            reachable.add(node_id)

            #meklē visas pārejas 
            for edge in self.diagram.edges:
                if edge.source == node_id and edge.target not in reachable:
                    dfs(edge.target)

        #meklēšana sākas no start mezgla
        dfs(start_id)

        #parbaude, kuri mezgli nav sasniedzami
        unreachable = [
            node.label for node in self.diagram.nodes
            if node.id not in reachable
            ]

        if unreachable:
            return [f"Nesasniedzams mezgls atrasts: {unreachable}"]
        return[]

#Analīzes funkcija
    def analyze(self):

        report = [] #ziņojums

    #self-loop pārbaude
        if self.detect_self_loops():
         report.append("Self-loop atrasts diagrammā.")

    #retry ciklu problemas
        report.extend(self.detect_retry_cycles())

    #nesasniedzamo mezglu problemas
        report.extend(self.detect_unreachable_nodes())

        return report #atgriež problemu sarakstu 