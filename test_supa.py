import requests
import os

with open('contas_pagar_etl.py', 'r', encoding='utf-8') as f:
    code = f.readlines()

url = None
key = None

for line in code:
    if line.startswith('SUPABASE_URL'):
        url = line.split('=')[1].strip().strip('\"').strip('\'')
    if line.startswith('SUPABASE_KEY'):
        key = line.split('=')[1].strip().strip('\"').strip('\'')

headers = {'apikey': key, 'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
r = requests.get(f'{url}/rest/v1/contas_pagar?codigo_lancamento_omie=eq.2475831265', headers=headers)
print(r.json())
