"""
Izmanto GROQ API,lai izskaidrotu atrastas problemas 
un generetu uzlabojumus

"""
from groq import Groq

#client = Groq(api_key="")

def explain_problems(problems: list[str]) -> str:
    text = "\n".join(f"- {p}" for p in problems)

    prompt = (
        "Atrastās problēmas aktivitāšu diagramma:\n"
        f"{text}\n\n"
        "Lūdzu izskaidro šīs problēmas vienkāršā, saprotamā un skaidrā valodā, norādot, kāpēc tas var radīt lietojamības riskus un kā tas ietekmē lietotāja pieredzi."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_improved_scenario(problems: list[str], nodes, edges, edge_explanations=None) -> str:
    node_list = "\n".join(f"- {n.label} ({n.type})" for n in nodes)
    read_edges = "\n".join(edge_explanations or [])

    prompt = (
        "Aktivitāšu diagramma (mezglu un pārejas):\n\n"
        f"Mezgli:\n{node_list}\n\n"
        f"Pāreju skaidrojums:\n{read_edges}\n\n"
        "Šīs ir atrastās problēmas:\n"
        + "\n".join(f"- {p}" for p in problems)
        +"\n\n"
        "Lūdzu izveido uzlabotu scenāriju, kas novērš šīs atrastās problēmas, saglabā sākotnējo funkcionalitāti un, lai scenārijs atbilst lietojamības principiem. Uzraksti scenāriju loģisku, secīgu un viegli uztveramu, parādot arī pārejas. "
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content