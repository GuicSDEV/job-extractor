from dotenv import load_dotenv
import anthropic
import json
from pathlib import Path


load_dotenv()                     


class ChatBot:
        def __init__(self,system:str,client:object,model:str ="claude-haiku-5-5"):
            
            self.save_chat: list[dict[str,str]] = []
            self.model = model
            self.system = system
            self.client = client
        def enviar(self, message:str) -> str:
            self.save_chat.append({"role":"user","content":message})
            answer = self.client.messages.create(model=self.model,system = self.system ,max_tokens = 2000,messages = self.save_chat)
            reply = ""
            for block in answer.content:
                  if block.type == "text":  
                    reply += block.text
            self.save_chat.append({"role":"assistant","content":reply})
            return reply
        def reset(self) -> None:
            self.save_chat = []
                
        
def read(path,bot):
                resultados = []
                arquivos_txt = path.glob("*.txt")
                for arquivo in arquivos_txt:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        text = f.read()
                    mensagem = f"<job>{text}</job>"
                    bot.reset()
                    reply = bot.enviar(mensagem)
                    dados = json.loads(reply)
                    resultados.append(dados)
        
                return resultados    
def salvar(resultado, path="resultado.json"):
      with open(path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
      
if __name__ == "__main__":
    



    client = anthropic.Anthropic()  
    system_prompt = '''Extract structured data from the job posting inside <job> tags. Return ONLY a JSON object, with no text before or after it, following this schema:
{"company": string, "role": string, "remote": boolean, "location": string or null, "stack": list of strings, "salary_min": integer or null, "salary_max": integer or null, "currency": string or null, "period": "hour" | "month" | "year" | null}
Rules:
- Use null when the information is not in the posting. Never guess.
- "stack" contains only concrete technologies: languages, frameworks, libraries, tools and platforms.
- If there is a single salary value, use it for both salary_min and salary_max.
- "currency" is the ISO code, like "USD" or "EUR".
Example:
<job>DataWave is hiring a remote Machine Learning Intern. You will build data pipelines in Python and SQL and train models with PyTorch. Pay: $25-30/hour.</job>
<json>{"company": "DataWave", "role": "Machine Learning Intern", "remote": true, "location": null, "stack": ["Python", "SQL", "PyTorch"], "salary_min": 25, "salary_max": 30, "currency": "USD", "period": "hour"}</json>
'''
    bot = ChatBot(system_prompt, client)
    
    caminho = Path(input("digite o nome da pasta: "))
    resultado = read(caminho,bot)
    print(resultado)

    resposta = input("Voce quer salvar o resultado em um .json: ")
    if resposta.lower() == "sim":
          salvar(resultado)
          print("resultado salvo")
    else:
          print("finalizando programa")
    
         
        
        
        