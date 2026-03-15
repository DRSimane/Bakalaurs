
#diagrammas imports
from test_data import create_login_flow

#analizes imports
from analyzer import UXAnalyzer 

#testesanas diagrammas izveide
diagram = create_login_flow()

#analizes objekta izveide
analyzer = UXAnalyzer(diagram)

#analizes izpilde
results = analyzer.analyze()

#rezultatu izdruka
if results:
    print("Atrastās problēmas:")
    for r in results:
        print("-", r)
else:
    print("Netika atrastas UX problēmas")