# Agente GenAI — Análise de E-Commerce
Agente de IA com capacidade Text-to-SQL para consultar e analisar dados de um e-commerce usando linguagem natural.
## Stack- Python 3.10+
- Google Gemini 2.5 Flash
- SQLite (banco.db — fornecido)
- google.genai, pandas, python-dotenv
## Como executar:
### 1. Clone o repositório
git clone https://github.com/adenilsonneto/agente-ecommerce.git
cd agente-ecommerce
### 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
### 3. Instale as dependências
pip install -r requirements.txt
### 4. Configure a API Key
Crie um arquivo .env na raiz do projeto:
GEMINI_API_KEY=sua_chave_aqui
Obtenha sua chave em: https://aistudio.google.com
### 5. Coloque o banco de dados
Copie o arquivo do seu banco de dados para a raiz do projeto.
### 6. Execute o agente
python agente.py
## Exemplos de perguntas
- "Quais são os 10 produtos mais vendidos?"
- "Qual estado tem mais consumidores?"
- "Qual é a média de avaliação dos pedidos?"
- "Quais categorias têm mais avaliações negativas?"
## Execute para conferir as respostas
python testar_sql.py
