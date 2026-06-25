import os
import requests
from dotenv import load_dotenv

load_dotenv(r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Grupo_Studio\omie-supabase-etl\.env')
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

# Procurar o cliente 3191107479
url = f'{SUPABASE_URL}/rest/v1/clientes_grupo?codigo_cliente_omie=eq.3191107479'
r = requests.get(url, headers=headers)
print('Cliente 3191107479:', r.json())

# Procurar na contas_receber_grupo os lanamentos
url2 = f'{SUPABASE_URL}/rest/v1/contas_receber_grupo?codigo_cliente_fornecedor=in.(3191107479,3190124247,3189401935)'
r2 = requests.get(url2, headers=headers)
receb = r2.json()
print('Lançamentos encontrados para esses clientes:', len(receb))
if len(receb) > 0:
    for rec in receb:
        print(f"Receb: {rec.get('codigo_lancamento_omie')} - {rec.get('valor_documento')} - ID CL: {rec.get('codigo_cliente_fornecedor')} - CNPJ_EMP: {rec.get('empresa_cnpj')}")
