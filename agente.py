import os
import json
from pdb import main
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import get_system_prompt
from database import executar_sql


load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

#TOOLS
def consultar_banco(sql: str) -> str: #executa um query sql no banvo de dados, para responder perguntas sobre: vendas, produtos, consumidores, vendedores ou avaliações
    resultado = executar_sql(sql)

    if not resultado["sucesso"]:
        return json.dumps({
            "erro": resultado["erro"],
            "mensagem": "Query falhou. Verifique a sintaxe e tente novamente."
        }, ensure_ascii=False)

    dados = resultado["dados"]
    if len(dados) > 50:
        dados = dados[:50]

    return json.dumps({
        "sucesso": True,
        "colunas": resultado["colunas"],
        "dados": dados,
        "total_linhas": resultado["total_linhas"]
    }, ensure_ascii=False, default=str)



CONFIG = types.GenerateContentConfig(
    system_instruction=get_system_prompt(),
    tools=[consultar_banco], #passa a função Python diretamente
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=False#o SDK executa as tools automaticamente
    )
)

class AgenteEcommerce:
    
    def __init__(self): #inicializa o agente e configura o modelo generativo
        self.chat = client.chats.create(
            model = "gemini-2.5-flash-lite",
            config = CONFIG
        )
        
    
    def perguntar(self, pergunta: str, verbose: bool = False) -> str: # método para processar a pergunta do usuário e gerar uma resposta usando o modelo generativo
        if verbose:
            print(f"\n[AGENTE] Processando: {pergunta}")

        tentativas = 3
        for i in range(tentativas):
            try:
                resposta = self.chat.send_message(pergunta)
                return resposta.text
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    #cota esgotada não adianta tentar de novo para nao perder mais requisições, então já retorna a mensagem de cota atingida
                    return "Cota da API atingida. Aguarde até 21h (horário de Brasília) para o reset diário."
                elif "503" in str(e) or "UNAVAILABLE" in str(e):
                    if i < tentativas - 1:
                        print(f"[AVISO] Servidor sobrecarregado. Tentando novamente em 10s... ({i+1}/{tentativas})")
                        time.sleep(10)
                    else:
                        return "O servidor está temporariamente indisponível. Tente novamente em alguns minutos."
                else:
                    raise e

    
    def resetar_conversa(self): #método para resetar o histórico da conversa
        print("Histórico da conversa resetado.")
        self.chat = client.chats.create(
            model="gemini-2.5-flash",
            config=CONFIG
        )
        print("Conversa reiniciada.")
        
def main(): #função principal para testar o agente
    
    print("Agente de Análise de dados para E-commerce")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("Digite 'reset' para para limpar o histórico da conversa.")

    agente = AgenteEcommerce() #instancia o agente e inicia o loop de interação com o usuário
    
    while True:
        pergunta = input("Você: ").strip()

        if not pergunta:
            continue
        if pergunta.lower() == 'sair':
            print("Encerrando a conversa. Até mais!")
            break
        if pergunta.lower() == 'reset':
            agente.resetar_conversa()
            print("Histórico da conversa limpo. Pode começar uma nova conversa.")
            continue

        print("\nAgente: ", end="", flush=True)
        resposta = agente.perguntar(pergunta, verbose=True)
        print(resposta)
        print()

if __name__ == "__main__":
    main()