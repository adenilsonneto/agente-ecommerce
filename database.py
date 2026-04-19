import sqlite3
import pandas as pd
from typing import Optional
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco.db") #procura o banco na mesma pasta que o script database.py

def executar_sql(sql: str) -> list: #executa uma query SQL e retorna uma lista de dicionarios
    try:
        conn = sqlite3.connect(DB_PATH)
        sql_upper = sql.strip().upper()
        if any(sql_upper.startswith(op) for op in ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER']):
            return {"sucesso": False,
                    "erro": "Operação não permitida: apenas consultas SELECT são permitidas.",
                    "dados": [],
                    "colunas":  []}
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return {
            "sucesso": True,
            "dados": df.to_dict(orient='records'),
            "colunas": list(df.columns),
            "total_linhas": len(df)
        }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
            "dados": [],
            "colunas": []
        }

def get_schema_completo() -> str: #retorna o schema completo do banco de dados como texto
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in cursor.fetchall()]
    schema = []
    
    for tabela in tabelas:
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = cursor.fetchall()
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
        total = cursor.fetchone()[0]
        schema.append(f"\nTabela: {tabela} ({total:,} registros)")
        
        for coluna in colunas:
            schema.append(f"  - {coluna[1]} ({coluna[2]})")
        
        conn.close()

        return "\n".join(schema)




