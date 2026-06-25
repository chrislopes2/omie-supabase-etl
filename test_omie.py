import requests

url = 'https://app.omie.com.br/api/v1/financas/contapagar/'
body = {
    'call': 'ListarContasPagar',
    'app_key': '2790372542958',
    'app_secret': 'e5b71f2190f482fb37aefdf793a124c1',
    'param': [{
        'pagina': 1,
        'registros_por_pagina': 100,
        'apenas_importado_api': 'N'
    }]
}
r = requests.post(url, json=body)
if r.status_code == 200:
    data = r.json()
    print(f"Total de Páginas na Omie: {data.get('total_de_paginas')}")
    print(f"Total de Registros na Omie: {data.get('total_de_registros')}")
    
    # Vamos caçar o Henri em TODAS as páginas
    henri_found = False
    for pagina in range(1, data.get('total_de_paginas', 1) + 1):
        body['param'][0]['pagina'] = pagina
        r_pag = requests.post(url, json=body)
        if r_pag.status_code == 200:
            data_pag = r_pag.json()
            if 'conta_pagar_cadastro' in data_pag:
                for c in data_pag['conta_pagar_cadastro']:
                    if str(c.get('codigo_lancamento_omie')) == '2475831265':
                        print(f"ACHEI O HENRI NA PÁGINA {pagina}! Venc: {c.get('data_vencimento')}")
                        henri_found = True
    if not henri_found:
        print("HENRI NÃO VEIO NA LISTAGEM GERAL DA OMIE!")
else:
    print('Erro na API:', r.text)
