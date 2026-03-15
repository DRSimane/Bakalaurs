
#definēto klašu importācija
from models import Node, Edge, ActivityDiagram

# funkcija, kas izveido vienkāršu login plūsmu 
def create_login_flow():

    # mezglu definēšana(diagrammas punkti)
    nodes = [
        Node("1", "Start", "start"),                #Sakuma mezgls
        Node("2", "Login Page", "action"),          #log in lapa
        Node("3", "Enter Credentials", "action"),   # lietotajs ievada datus
        Node("4", "Error Message", "action"),       # paradas kluda
        Node("5", "Dashboard", "end"),              # Veiksmiga autorizacija
        ]

    #parejas starp mezgliem
    edges = [
        Edge("1", "2"),                 #Start -> Login
        Edge("2", "3"),                 #Login -> Enter cred
        Edge("3", "3"),
        Edge("3", "4", "invalid"),      #Ja dati nepareizi -> Error
        Edge("4", "2", "retry"),        #Retry -> atpakal uz login
        Edge("3", "5", "valid"),        #Ja dati pareizi -> Dashboard
        ]

    #Atgriez pilu diagrammu
    return ActivityDiagram(nodes, edges)
