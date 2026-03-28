
# Diagrammas modeļa imports
from models import ActivityDiagram

#Klase, kas veic UX analīzi 
class UXAnalyzer:

    #Konstruktors saņem diagrammu
    def __init__(self, diagram: ActivityDiagram):
        self.diagram = diagram # saglaba diagrammu ieksejai lietosanai
    
    #Pirmais kritērijs - Sistēma stāvokļa redzamība

    #Mezgls, kas aizved pats uz sevi
    def detect_self_loops(self):
        loops = [] #saraksts atrastajiem cikliem

        #iteracija caur visam parejam
        for edge in self.diagram.edges:

            #ja pārejas sakuma un beigu mezgls sakrīt 
            if edge.source == edge.target:
                loops.append(f"Self-loop mezgls: {edge.source}") #saglaba ka problemu 

        return loops #Atgriež atrastos ciklus 
    
    #Mezgls bez izejošām pārejām(neiekļaujot end mezglu)
    def detect_nodes_without_outgoing(self):
        problems = []
        outgoing = {e.source for e in self.diagram.edges}
        for node in self.diagram.nodes:
            if node.id not in outgoing and node.type != "end":
                problems.append(f"Mezglam '{node.label}' nav izejošu pareju.")
        return problems
    
    #Bezgalīgi cikli
    def detect_infinite_cycles(self):
        problems = []
        visited = set()
        stack = set()
        reported = set()

        def dfs(node_id):
            if node_id in stack:
                if node_id not in reported:
                    problems.append("Atrasts potenciāls bezgalīgs cikls")
                    reported.add(node_id)
                return
            stack.add(node_id)
            for e in self.diagram.edges:
                if e.source == node_id:
                    dfs(e.target)
            stack.remove(node_id)

        for n in self.diagram.nodes:
            dfs(n.id)

        return problems
    
    #Retry cikli bez alternatīvas izejas
    def detect_retry_cycles(self):
        problems = []
        for edge in self.diagram.edges:
            if edge.condition == "retry":
                problems.append("Iespējams bezgalīgs retry cikls")
        return problems
    
    #Otrais kritērijs - Atbilstība mentālajiem modeļiem
    
    #mezgls bez ienākošām pārejām(neieskaitot start mezglu)
    def detect_nodes_without_incoming(self):
        problems = []
        incoming = {e.target for e in self.diagram.edges}
        for node in self.diagram.nodes:
            if node.id not in incoming and node.type != "start":
                problems.append(f"Mezglam '{node.label}' nav ienākošu pāreju.")
            return problems
        
    # Vairāk nekā viens start mezgls
    def detect_multiple_start_nodes(self):
        starts = [n for n in self.diagram.nodes if n.type == "start"]
        if len(starts) > 1:
            return("Diagrammā ir vairāk nekā viens sākuma mezgls.")
        return []
    
    # Neatbilstoši mezgli(piemēram, pēc beigu mezgla ir pāreja)
    def detect_invalid_node_sequences(self):
        problems = []
        for edge in self.diagram.edges:
            source = next(n for n in self.diagram.nodes if n.id == edge.source)
            if source.type == "end":
                problems.append("Pēc beigu mezgla nedrīkst būt pārejas.")
        return problems
    
    # 3.kritērijs - Lietotāja kontrole un brīvība
    # Mezgls, kurš nekur neved
    def detect_dead_ends(self):
        problems = []
        outgoing = {e.source for e in self.diagram.edges}
        for node in self.diagram.nodes:
            problems.append(f"Mezgls '{node.label}' ir strupceļš.")
        return problems
    
    #4.kritērijs - konsekvence un standarti
    #Izveles mezgls bez nosacījumiem
    def detect_decisions_without_conditions(self):
        problems = []
        for node in self.diagram.nodes:
            if node.type == "decision":
                outgoing = [e for e in self.diagram.edges if e.source == node.id]
                for e in outgoing:
                    if not e.condition:
                        problems.append(f"Izvēles mezglam '{node.label}' nav nosacījuma.")
        return problems
    
    # Nekonsekventi nosacījumi
    def detect_inconsistent_conditions(self):
        problems = []
        allowed = ["valid", "invalid", "retry"]
        for edge in self.diagram.edges:
            if edge.condition and edge.condition not in allowed:
                problems.append(f"Nekonsekvents nosacījums: {edge.condition}")
        return problems
    
    #5.Kritērijs - Atmiņas slodzes samazināšana
    #Mezgls ar parāk daudz izejām 
    def detect_nodes_with_many_exits(self):
        problems = []
        for node in self.diagram.nodes:
            outgoing = [e for e in self.diagram.edges if e.source == node.id]
            if len(outgoing) > 3:
                problems.append(f"Mezglam '{node.label}' ir pārāk daudz izeju ({len(outgoing)}).")
        return problems
    
    #pārāk gara plūsma 
    def detect_long_flow(self):
        if len(self.diagram.nodes) > 20:
            return ["Plūsma ir pārak gara un var radīt kognatīvo slodzi."]
        return []
    
    #Pārāk daudz lēmumu mezglu 
    def detect_too_many_decisions(self):
        decisions = [n for n in self.diagram.nodes if n.type == "decision"]
        if len(decisions) > 5:
            return ["Parāk daudz lēmumu mezglu plūsmā."]
        return []
    
    #6.kritērijs - elastība un efektivitāte
    #tikai viens ceļš no sākuma līdz beigām
    def detect_single_path(self):
        #ja tikai viens valid ceļš
        valid_edges = [e for e in self.diagram.edges if e.condition == "valid"]
        if len(valid_edges) <= 1:
            return ["Plūsmai ir tikai viens ceļš - trūkst alternatīvu"]
        return []
    
    #Nav īsceļu
    def detect_no_shorcut(self):
        #shortcut = pāreja, kas izlaiž mezglus
        problems = []
        for edge in self.diagram.edges:
            if edge.source.startswith("1") and edge.target.startswith("5"):
                problems.append("Plūsmā nav īsceļu.")
        return problems
    
    #7.Kritērijs - minimalistisks dizains
    #Neizmantoti mezgli 
    def detect_unused_nodes(self):
        used = {e.source for e in self.diagram.edges} | {e.target for e in self.diagram.edges}
        problems = []
        for node in self.diagram.nodes:
            if node.id not in used:
                problems.append(f"Mezgls '{node.label} netiek izmantots.")
        return problems
    
    #8.kritērijs - kļūdu mezglu pārbauda
    #kļūdu mezgli bez izejas 
    def detect_error_nodes_without_exit(self):
        problems = []
        for node in self.diagram.nodes:
            if "error" in node.label.lower():
                outgoing = [e for e in self.diagram.edges if e.source == node.id]
                if not outgoing:
                    problems.append(f"Kļudu mezglam '{node.label}' nav izejas.")
        return problems
    
    #Kļūdu mezgli, kas ved uz atkal mēģināšanu
    def detect_error_retry_loops(self):
        problems = []
        for node in self.diagram.nodes:
            if "error" in node.label.lower():
                outgoing = [e for e in self.diagram.edges if e.source == node.id]
                if outgoing and all(e.condition == "retry" for e in outgoing):
                    problems.append(f"Kļūdas mezgls '{node.label}' ved tikai uz atkārtošanu.")
        return problems
    
    #9.kriterijs - palīdzība
    def detect_help_nodes(self):
        help_nodes = [n for n in self.diagram.nodes]
        if not help_nodes:
            return ["Plūsma nav palidzības mezgla."]
        return []

#10 kriterijs - Vizuālā uztveramība
    def detect_visual_clarity(self):
        return []
    
    #11.Kriterijs noslēgtība 
    def detect_missing_end(self):
        ends = [n for n in self.diagram.nodes if n.type == "end"]
        if not ends:
            return ["Plūsmai nav beigu mezgla."]
        return []
    
    #analīzes funkcija
    def analyze(self):
        report = []

        #1.kriterijs
        report.extend(self.detect_self_loops())
        report.extend(self.detect_nodes_without_outgoing())
        report.extend(self.detect_infinite_cycles())
        report.extend(self.detect_retry_cycles())

        #2.kriterijs
        report.extend(self.detect_nodes_without_incoming())
        report.extend(self.detect_multiple_start_nodes())
        report.extend(self.detect_invalid_node_sequences())

        #3.kriterijs
        report.extend(self.detect_dead_ends())

        #4.kriterijs
        report.extend(self.detect_decisions_without_conditions())
        report.extend(self.detect_inconsistent_conditions())

        #5.kriterijs
        report.extend(self.detect_nodes_with_many_exits())
        report.extend(self.detect_long_flow())
        report.extend(self.detect_too_many_decisions())

        #6.kriterijs
        report.extend(self.detect_single_path())
        report.extend(self.detect_no_shorcut())

        #7.kriterijs
        report.extend(self.detect_unused_nodes())

        #8.kriterijs
        report.extend(self.detect_error_nodes_without_exit())
        report.extend(self.detect_error_retry_loops())

        #9.kriterijs
        report.extend(self.detect_help_nodes())

        #10.kriterijs
        report.extend(self.detect_visual_clarity())

        #11.kriterijs
        report.extend(self.detect_missing_end())

        return report