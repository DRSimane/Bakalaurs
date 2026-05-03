#analizes imports
from analyzer import UXAnalyzer 
from parser import load_diagram_from_drawio_xml
from ai_generator import explain_problems, generate_improved_scenario

def main():
    path = "otraisTestScen.drawio"

    diagram =load_diagram_from_drawio_xml(path)

    #analizes objekta izveide
    analyzer = UXAnalyzer(diagram)

    #analizes izpilde
    results = analyzer.analyze()

    #rezultatu izdruka
    if results:
        print("Atrastās problēmas:")
        for r in results:
            print("-", r)

        print("\nAI skaidrojums:")
        print(explain_problems(results))

        edge_explanations = diagram.explain_edges_readable()

        print("\nAI ģenerēts labojums:")
        print(generate_improved_scenario(
        results, 
        diagram.nodes, 
        diagram.edges,
        edge_explanations=edge_explanations
        ))

    else:
        print("Netika atrastas UX problēmas")

if __name__ == "__main__":
    main()