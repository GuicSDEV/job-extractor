
import json

seen = {}




arquivo = input("qual o arquivo que vc quer analisar: ")
with open(arquivo, "r", encoding="utf-8") as entrada:
    dados = json.load(entrada)


for vaga in dados:
    for tech in vaga["stack"]:
        tech = tech.lower()
        if tech in seen:
            seen[tech] +=1
        else:
            seen[tech] = 1


ranking=sorted(seen.items(),key =lambda p: p[1],reverse=True)
print(ranking[:10])

