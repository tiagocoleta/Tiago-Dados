# gerar_base_suja.py
import pandas as pd
import numpy as np

# Criando dados sujos fictícios (focados em governo)
data = {
    'id_servidor': ['S01', ' S02', 'S03 ', 'S01', 'S04', 'S05'],
    'data_nascimento': ['10/05/1980', '1982-01-15', '01-20-1985', np.nan, '1990/03/10', '01/01/2000'],
    'orgao_origem': ['SAP', 'SAUDE', 'sap', ' Infra', 'RH', 'saude '],
    'salario_bruto': ['R$ 5.000,00', '6000.00', ' 4500,50', '5000', '7100.20', 'np.nan']
}

# Criando o DataFrame
df_sujo = pd.DataFrame(data)

# Salvando como um CSV sujo
df_sujo.to_csv('base_servidores_suja.csv', index=False, sep=';', encoding='latin1')

print("Base 'base_servidores_suja.csv' gerada com sucesso na pasta!")
print(df_sujo)