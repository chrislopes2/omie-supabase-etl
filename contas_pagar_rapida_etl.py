import contas_pagar_etl

# Focar apenas na empresa que tem os lançamentos problemáticos
contas_pagar_etl.EMPRESAS = [
    { "empresa": "STUDIO OPERACIONAL", "cnpj": "23.448.109/0001-91", "app_key": "2904360428970", "app_secret": "fbc75836f2a73b196223b5b589306c47" }
]

if __name__ == "__main__":
    contas_pagar_etl.rodar_rotina_cp()
