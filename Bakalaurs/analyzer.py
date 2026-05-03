
# Diagrammas modeļa imports
from models import ActivityDiagram

#Klase, kas veic UX analīzi 
class UXAnalyzer:

    #Konstruktors saņem diagrammu
    def __init__(self, diagram: ActivityDiagram):
        self.diagram = diagram # saglaba diagrammu ieksejai lietosanai
        self.node_map = {n.id: n.label for n in diagram.nodes}
    
    #Pirmais kritērijs - Sistēma stāvokļa redzamība

    #Mezgls, kas aizved pats uz sevi
    def detect_self_loops(self):
        loops = [] #saraksts atrastajiem cikliem

        #iteracija caur visam parejam
        for e in self.diagram.edges:

            #ja pārejas sakuma un beigu mezgls sakrīt 
            if e.source == e.target:
                label = self.node_map.get(e.source, e.source)
                loops.append(f"Self-loop mezgls: {label}") #saglaba ka problemu 

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
        reported = False   

        def dfs(node_id):
            nonlocal reported

            # ja jau ziņots
            if reported:
                return

            if node_id in stack:
                # parbaude vai nav retry cikls
                label = self.node_map.get(node_id, node_id)
                problems.append(f"Atrasts potenciāls bezgalīgs cikls - {label}")
                reported = True
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
                label = self.node_map.get(edge.source, edge.source)
                problems.append(f"Iespējams bezgalīgs retry cikls - '{label}'.")
        return problems
    
    #plūsmas sadalei jābūt vismaz divām izejām
    def detect_invalid_fork_nodes(self):
        problems = []
        for node in self.diagram.nodes:
            if node.type == "fork":
                outgoing = [e for e in self.diagram.edges if e.source == node.id]
                if len(outgoing) < 2:
                    problems.append(f"Plūsmas sadalei jābūt vismaz divām izejām.")
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
            target = next(n for n in self.diagram.nodes if n.id == edge.target)
            if source.type == "end":
                problems.append(f"Pēc beigu mezgla nedrīkst būt pārejas.")
            if target.type == "start":
                problems.append(f"Sākuma mezglam nedrīkst būt ienākošās pārejas.")
        return problems
    
    def detect_invalid_join_nodes(self):
        problems = []
        for node in self.diagram.nodes:
            if node.type == "join":
                incoming = [e for e in self.diagram.edges if e.target == node.id]
                if len(incoming) < 2:
                    problems.append(f"Join mezglam jābūt vismaz divām ienākošām pārejām.")
        return problems

    
    # 3.kritērijs - Lietotāja kontrole un brīvība
    # Mezgls, kurš nekur neved
    def detect_dead_ends(self):
        problems = []

        for node in self.diagram.nodes:
            outgoing = [e for e in self.diagram.edges if e.source == node.id]

            # START mezglam drīkst nebūt incoming
            if node.type == "start":
                continue

            # END mezglam drīkst nebūt outgoing
            if node.type == "end":
                continue

            # ERROR mezglam drīkst būt tikai retry
            if node.type == "error":
                # ja error mezgls nekur neved → tā ir problēma
                if not outgoing:
                    problems.append(f"Kļūdu mezgls '{node.label}' ir strupceļš.")
                continue

            # ACTION mezgls nav strupceļš, ja tas ved uz END
            if node.type == "action":
                if not outgoing:
                    problems.append(f"Mezgls '{node.label}' ir strupceļš.")
                continue

            # DECISION mezglam jābūt vismaz 2 izejām
            if node.type == "decision":
                if len(outgoing) < 2:
                    problems.append(f"Izvēles mezglam '{node.label}' nav pietiekamu izeju.")
                continue

        return problems
    
    def detect_fork_join_pairing(self):
        problems = []
        forks = [n for n in self.diagram.nodes if n.type == "fork"]
        joins = [n for n in self.diagram.nodes if n.type == "join"]

        if forks and not joins:
            problems.append("Diagrammā ir plūsmas sadalīšana, bet nav savienošanas.")
        if joins and not forks:
            problems.append("Diagrammā ir plūsmas savienošana, bet nav sadalīšana.")

        return problems

    
    #4.kritērijs - konsekvence un standarti
    #Izveles mezgls bez nosacījumiem
    def detect_decisions_without_conditions(self):
        problems = []
        for node in self.diagram.nodes:
            if node.type == "decision":
                outgoing = [e for e in self.diagram.edges if e.source == node.id]
                if not any(e.condition for e in outgoing):
                    problems.append("Izvēles mezglam nav nosacījuma.")
        return problems
    
    def detect_parallel_flow_integrity(self):
        problems = []

        forks = [n for n in self.diagram.nodes if n.type == "fork"]

        for fork in forks:
            outgoing_edges = [e for e in self.diagram.edges if e.source == fork.id]
            branch_targets = [e.target for e in outgoing_edges]

            for branch in branch_targets:
                next_edges = [e for e in self.diagram.edges if e.source == branch]

                leads_to_join = False
                for e in next_edges:
                    target_node = next((n for n in self.diagram.nodes if n.id == e.target), None)
                    if target_node and target_node.type == "join":
                        leads_to_join = True
                        break

                if not leads_to_join:
                    problems.append(
                    f"Plūsmas sadales izeja nenonāk plūsmas apvienošanā."
                    )

        return problems


    
    #5.Kritērijs - Atmiņas slodzes samazināšana
    #Mezgls ar parāk daudz izejām 
    def detect_nodes_with_many_exits(self):
        problems = []
        for node in self.diagram.nodes:
            outgoing = [e for e in self.diagram.edges if e.source == node.id]

            if node.type == "end" and len(outgoing) > 0:
                problems.append ("Beigu mezglam nedrīkst būt vairākas izejas")
                continue
            if node.type == "start" and len(outgoing) > 1:
                problems.append ("Sākuma mezglam drīkst būt tikai viena izeja")
                continue
            if node.type == "action" and len(outgoing) > 1:
                problems.append (f"Darbībai '{node.label}' drīkst būt tikai viena izeja.")
                continue
            if node.type == "decision": 
                if len(outgoing) < 2:
                    problems.append ("Izvēles mezglam jābūt vismaz divām izejām.")
                continue
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
        #ja nav nosacijumu, kriteriju nepiemero
        if not any(e.condition for e in self.diagram.edges):
            return[]

        #ja tikai viens valid ceļš
        valid_edges = [e for e in self.diagram.edges if e.condition == "valid"]
        if len(valid_edges) <= 1:
            return ["Plūsmai ir tikai viens ceļš - trūkst alternatīvu"]
        return []
    
    #Nav īsceļu
    def detect_no_shorcut(self):
        #shortcut = pāreja, kas izlaiž mezglus
        shortcuts = []
        for edge in self.diagram.edges:
            try:
                source_num = int(edge.source)
                target_num = int(edge.target)
            except ValueError:
                continue
            if target_num - source_num > 1:
               shortcuts.append((edge.source, edge.target))
        return []
    
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
        help_nodes = [n for n in self.diagram.nodes if "help" in n.label.lower()]
        if not help_nodes:
            return ["Plūsmā nav palidzības mezgla."]
        return []

#10 kriterijs - Vizuālā uztveramība
    def detect_visual_clarity(self):
        problems = []
        nodes = self.diagram.nodes
        edges = self.diagram.edges

        node_index = {node.id: i for i, node in enumerate(nodes)}

        #parbauda pareju skaitu attieciba pret mezglie
        if len(edges) > len(nodes) * 3:
            problems.append("Diagramma ir pārblīvēta jeb pāreju skaits ir pārāk liels attiecībā pret mezgliem.")
        
        #Mezgli ar parak daudz savienojumiem
        for node in nodes:
            incoming = [e for e in edges if e.target == node.id]
            outgoing = [e for e in edges if e.source == node.id]

            total_connections = len(incoming) + len(outgoing)

            if total_connections > 6:
                problems.append(f"Mezgls '{node.label}:' ir pārslogots, tam ir {total_connections} savienojumi.")

            #pārbaude vai pārejas neiet atpakaļ
        for edge in edges:
            if node_index[edge.target] < node_index[edge.source]:
                problems.append(f"Pāreja no '{self.node_map[edge.source]}' uz '{self.node_map[edge.target]}' iet atpakaļ.")
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
        report.extend(self.detect_invalid_fork_nodes())

        #2.kriterijs
        report.extend(self.detect_nodes_without_incoming())
        report.extend(self.detect_multiple_start_nodes())
        report.extend(self.detect_invalid_node_sequences())
        report.extend(self.detect_invalid_join_nodes())

        #3.kriterijs
        report.extend(self.detect_dead_ends())
        report.extend(self.detect_fork_join_pairing())

        #4.kriterijs
        report.extend(self.detect_decisions_without_conditions())
        report.extend(self.detect_parallel_flow_integrity())

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