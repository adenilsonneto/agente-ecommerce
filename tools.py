from database import executar_sql
import json

def consultar_banco(sql: str) -> str: #função para consultar o banco de dados e retornar os resultados em formato JSON
    resultado = executar_sql(sql)
    if not resultado["sucesso"]:
        return json.dumps({
            "erro": resultado["erro"],
            "mensagem": "A consulta falhou. Verifique a sintaxe SQL e tente novamente."
        }, ensure_ascii=False)
    dados = resultado["dados"] 
    if len(dados) > 50:
        dados = dados[:50] #limita a resposta para nao explodir o contexto do modelo
        resultado = {"aviso": f"Resultado limitado a 50 linhas. Total de linhas: {resultado['total_linhas']}"}
        return json.dumps({
            "sucesso": True,
            "colunas": resultado["colunas"],
            "dados": dados,
            "total_linhas": resultado["total_linhas"],
        }, ensure_ascii=False, default=str)

#declaração da função para o modelo, seguindo o formato esperado pela API do Gemini
#basicamente o que o gemini lê para entender a tool
TOOL_DECLARATION = { 
    "function_declarations": [
        {
            "name": "consultar_banco",
            "description": "Executa uma query SQL SELECT no banco de dados do e-commerce e retorna os resultados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "Query SQL SELECT válida para o banco SQLite"
                    }
                },
                "required": ["sql"]
            }
        }
    ]
}