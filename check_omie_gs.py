import requests

url_cr = 'https://app.omie.com.br/api/v1/financas/contareceber/'
payload = {
    'call': 'ListarContasReceber',
    'app_key': '2858651808012',
    'app_secret': '06a62c592967ba7c20331f486fb735f5',
    'param': [{'pagina': 1, 'registros_por_pagina': 500, 'filtrar_por_data_de': '01/06/2026', 'filtrar_por_data_ate': '30/06/2026'}]
}
r = requests.post(url_cr, json=payload)
data = r.json()
if 'conta_receber_cadastro' in data:
    for c in data['conta_receber_cadastro']:
        if c.get('valor_documento') in [1997.6, 1497.0, 1404.93, 1497]:
            print(f"Receita {c.get('valor_documento')} no dia {c.get('data_emissao')} -> Cliente_Fornecedor: {c.get('codigo_cliente_fornecedor')} - {c.get('codigo_lancamento_omie')}")
else:
    print('Sem contas nesse periodo 2026:', data)
