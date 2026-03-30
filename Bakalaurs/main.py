#analizes imports
from analyzer import UXAnalyzer 
from parser import load_diagram_from_drawio_xml
from ai_generator import explain_problems, generate_improved_scenario

def main():
    path = "diagram.drawio"

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
        explanation = explain_problems(results)
        print(explanation)

        print("\nAI ģenerēts labojums:")
        improved = generate_improved_scenario(results, diagram.nodes, diagram.edges)
        print(improved)
    else:
        print("Netika atrastas UX problēmas")

if __name__ == "__main__":
    main()