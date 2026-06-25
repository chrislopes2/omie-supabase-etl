import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

response = supabase.table('contas_receber_grupo')\
    .select('codigo_lancamento_omie, codigo_cliente_fornecedor, empresa_nome, data_emissao, valor_documento')\
    .eq('empresa_nome', 'BRAGA E MONTEIRO')\
    .eq('valor_documento', 1175.15)\
    .execute()

print("Lancamento:")
print(response.data)

if response.data:
    cliente_id = response.data[0]['codigo_cliente_fornecedor']
    cliente_resp = supabase.table('clientes_grupo')\
        .select('*')\
        .eq('codigo_cliente_omie', cliente_id)\
        .execute()
    print("Cliente associado:")
    print(cliente_resp.data)
