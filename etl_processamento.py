# etl_processamento.py
import pandas as pd
import numpy as np
import os

# 1. EXTRACT (Extração do Legado)
print("--- Iniciando Extração ---")
# Lendo o CSV sujo (Entendendo encoding e separador)
try:
    df = pd.read_csv('base_servidores_suja.csv', sep=';', encoding='latin1')
except FileNotFoundError:
    print("Arquivo sujo não encontrado. Rode o script de geração primeiro.")
    os._exit(0)

# 2. TRANSFORM (Saneamento/Limpeza)
print("--- Iniciando Transformação (Saneamento) ---")

# A. Limpeza de IDs e Strings (Removendo espaços e padronizando Órgãos)
# Essencial para garantir integridade na centralização
df['id_servidor'] = df['id_servidor'].str.strip()
df['orgao_origem'] = df['orgao_origem'].str.strip().str.upper()

# B. Padronização de Datas (ISO 8601) - Crítico para sistemas legados
# Usamos coerce para transformar erros em NaN
df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], dayfirst=True, errors='coerce')

# C. Tratamento Financeiro (Removendo R$ e padronizando float)
# Sistemas antigos muitas vezes misturam formatos de moeda
df['salario_bruto'] = df['salario_bruto'].astype(str).str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.').astype(float)

# D. Tratamento de Nulos e Duplicatas
# Removemos a duplicata óbvia do S01
df = df.drop_duplicates(subset=['id_servidor'], keep='first')
# Preenchemos salários nulos com a média (Imputação simples para demonstração)
mean_salary = df['salario_bruto'].mean()
df['salario_bruto'].fillna(mean_salary, inplace=True)

# 3. LOAD (Carga para Centralização)
print("--- Iniciando Carga ---")
# Salvando a base limpa e padronizada
df.to_csv('base_servidores_limpa.csv', index=False, sep=',', encoding='utf-8')

print("--- ETL Concluído com Sucesso ---")
print("Arquivo 'base_servidores_limpa.csv' gerado!")
print(df)