# centralizacao_dados.py
import sqlite3
import pandas as pd
import os

# 1. Carregando a base já limpa (do Projeto 1)
print("--- Carregando Base de Servidores (Limpa) ---")
try:
    df_servidores = pd.read_csv('base_servidores_limpa.csv')
except FileNotFoundError:
    print("Arquivo 'base_servidores_limpa.csv' não encontrado. Copie-o do Projeto 1.")
    os._exit(0)

# 2. Simulando uma segunda base de outra secretaria (ex: RH - Ativos de TI)
# Esta base demonstra a heterogeneidade dos dados de governo
print("--- Simulando Base de Ativos (RH) ---")
data_ativos = {
    'id_servidor': ['S01', 'S02', 'S03', 'S04', 'S05'],
    'ativo_ti': ['Notebook Dell', 'Desktop HP', 'Notebook Lenovo', 'MacBook Air', 'Nenhum'],
    'status_ativo': ['Ativo', 'Ativo', 'Em Manutenção', 'Ativo',3000]
}
df_ativos = pd.DataFrame(data_ativos)

# 3. INTEROPERABILIDADE: Centralização via SQL (SQLite em memória)
# Esta etapa prova a capacidade técnica de usar SQL para integrar bases
print("--- Realizando Centralização via SQL ---")
# Criando conexão com banco em memória (perfeito para testes rápidos)
conn = sqlite3.connect(':memory:')

# Salvando os DataFrames como tabelas SQL
df_servidores.to_sql('servidores', conn, index=False)
df_ativos.to_sql('ativos', conn, index=False)

# A Mágica do SQL: JOIN para interoperabilidade
# Estamos unindo as duas bases pela chave comum 'id_servidor'
query = """
SELECT s.id_servidor, s.orgao_origem, a.ativo_ti, a.status_ativo
FROM servidores s
JOIN ativos a ON s.id_servidor = a.id_servidor
WHERE a.status_ativo IS NOT NULL
"""

# Executando a query e voltando para Pandas
df_centralizado = pd.read_sql(query, conn)

# 4. Exportação da Base Centralizada
# Esta base representa o "Golden Record" unificado do Estado
print("--- Exportando Base Centralizada ---")
df_centralizado.to_csv('base_centralizada_final.csv', index=False)

print("--- Centralização Concluída ---")
print("Arquivo 'base_centralizada_final.csv' gerado!")
print(df_centralizado)