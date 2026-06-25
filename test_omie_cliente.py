import requests

url = 'https://app.omie.com.br/api/v1/geral/clientes/'
body = {
    "call": "ConsultarCliente",
    "app_key": "2790372542958",
    "app_secret": "e5b71f2190f482fb37aefdf793a124c1",
    "param": [{
        "codigo_cliente_omie": 2475830992
    }]
}

r = requests.post(url, json=body)
print(r.status_code)
print(r.text)
