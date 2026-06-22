import os
import requests
import time
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: Variáveis de ambiente SUPABASE_URL ou SUPABASE_KEY não configuradas.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Mesmas empresas do main.py
EMPRESAS = [
    {"empresa": "ALIANÇA LEGAL", "app_key": "3834645228678", "app_secret": "3127dd0e7371ed5ce40ef0f0c05cd9c4", "cnpj": "40316410000100"},
    {"empresa": "AUDIT TECNOLOGIA", "app_key": "3834648118029", "app_secret": "44dfa7593c1356f913d80b435f3752e2", "cnpj": "40321267000107"},
    {"empresa": "BRAGA E MONTEIRO", "app_key": "1298453472099", "app_secret": "fc3bb203e012e8b2ed3b934ec710b719", "cnpj": "08031102000185"},
    {"empresa": "E-FISCAL OPERACIONAL", "app_key": "3834642953259", "app_secret": "119fcdbf0954930bfcfddf946d849b2c", "cnpj": "40212048000115"},
    {"empresa": "FERREIRA & MONTEIRO", "app_key": "1298453471018", "app_secret": "6d98c5a2c4e8574345511e63a1523a65", "cnpj": "07450371000155"},
    {"empresa": "GS EDUCAÇÃO", "app_key": "3834645371694", "app_secret": "046d4c06f3630fbc982a5d2c0b4847da", "cnpj": "40306385000109"},
    {"empresa": "SF CONSULTORIA", "app_key": "3834642646399", "app_secret": "281f9bba97ab74cd78dd35a8220023ee", "cnpj": "40211756000130"},
    {"empresa": "SPACE W", "app_key": "3834642646294", "app_secret": "00a5d4a4f8da24bb6b2e1b8c00c73295", "cnpj": "40212133000183"},
    {"empresa": "STUDIO ADMINISTRAÇÃO", "app_key": "3834642953331", "app_secret": "ba47913cf0bafb4c4897082da2b7a4de", "cnpj": "40211933000113"},
    {"empresa": "STUDIO AGRONEGÓCIOS", "app_key": "3834645228807", "app_secret": "1df5d4a2503d2e96030cff0391d8bbcc", "cnpj": "40306466000109"},
    {"empresa": "STUDIO BANK", "app_key": "3834642953112", "app_secret": "942f7035677cece9e585e135cfecb457", "cnpj": "40212260000182"},
    {"empresa": "STUDIO BROKERS", "app_key": "3834645228695", "app_secret": "664c3c1db92c3a5ef52467d30d97fffa", "cnpj": "40306429000109"},
    {"empresa": "STUDIO CONTABILIDADE LTDA", "app_key": "2461014169543", "app_secret": "31ed2d6fbd5d72f5341cf63d043477d9", "cnpj": "23908861000160"},
    {"empresa": "STUDIO ENERGY", "app_key": "3834645228804", "app_secret": "2e7cfd395a12ce97274db2bb22a5ec7c", "cnpj": "40306477000199"},
    {"empresa": "STUDIO FACTORING", "app_key": "3834642953328", "app_secret": "2b9f36f6d63d6f14041b31d8e13d96ed", "cnpj": "40211849000164"},
    {"empresa": "STUDIO FISCAL", "app_key": "3834642953322", "app_secret": "d2ee7fbd30c0065a4c95dd7c4e511417", "cnpj": "40211867000146"},
    {"empresa": "STUDIO GROWTH", "app_key": "3834645228801", "app_secret": "3e9c20a4b884976451e06dce4495de1e", "cnpj": "40306489000113"},
    {"empresa": "STUDIO OPERACIONAL", "app_key": "3834645228675", "app_secret": "1e51fbbff5d90ee2b5f6390141154c55", "cnpj": "40306354000158"},
    {"empresa": "STUDIO OPERACIONAL 01", "app_key": "1298453472506", "app_secret": "f35a0ce97c41bf63675f0a2ba14a84e3", "cnpj": "08031102000266"},
    {"empresa": "STUDIO PAR", "app_key": "3834645228688", "app_secret": "3c914e6dcfcf633a921d3e1575c32e0c", "cnpj": "40306443000102"},
    {"empresa": "STUDIO FAMILY", "app_key": "3834645228810", "app_secret": "b5748805f77864f772421db02dd7b6ed", "cnpj": "40306456000165"},
    {"empresa": "STUDIO SBS STORE", "app_key": "3834642953337", "app_secret": "6eb689a710bbbf6272370ca3bf1d27f8", "cnpj": "40211902000127"},
    {"empresa": "STUDIO STORE", "app_key": "3834645371691", "app_secret": "4693b7ffc6499388df67f539958064dc", "cnpj": "40306398000188"},
    {"empresa": "STUDIO VAREJO", "app_key": "3834642953256", "app_secret": "6519213192dd6dfa3520dd11f53d71ff", "cnpj": "40212061000174"}
]

def puxar_departamentos_isolado(empresa_config):
    pagina = 1
    tem_mais = True
    total_paginas_conhecido = 999999
    todos_registros = []
    url = "https://app.omie.com.br/api/v1/geral/departamentos/"
    
    while tem_mais:
        body = {
            "call": "ListarDepartamentos",
            "app_key": empresa_config["app_key"],
            "app_secret": empresa_config["app_secret"],
            "param": [{"pagina": pagina, "registros_por_pagina": 100}]
        }
        
        sucesso_na_pagina = False
        for tentativa in range(10): # Segurança extra com 10 tentativas
            try:
                response = requests.post(url, json=body, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if "departamentos" in data and len(data["departamentos"]) > 0:
                        for dept in data["departamentos"]:
                            registro = {
                                "codigo": dept.get("codigo"),
                                "empresa_nome": empresa_config["empresa"],
                                "empresa_cnpj": empresa_config["cnpj"],
                                "descricao": dept.get("descricao"),
                                "estrutura": dept.get("estrutura"),
                                "inativo": dept.get("inativo")
                            }
                            todos_registros.append(registro)
                        sucesso_na_pagina = True
                        pagina += 1
                        total_paginas_conhecido = data.get('total_de_paginas', total_paginas_conhecido)
                        break
                    else:
                        tem_mais = False
                        sucesso_na_pagina = True
                        total_paginas_conhecido = data.get('total_de_paginas', total_paginas_conhecido)
                        break
                else:
                    print(f"Tentativa {tentativa+1} falhou na página {pagina} com status {response.status_code}. Retentando em 5s...")
                    time.sleep(5)
            except Exception as e:
                print(f"Tentativa {tentativa+1} falhou na página {pagina} com erro: {e}. Retentando em 5s...")
                time.sleep(5)
                
        if not sucesso_na_pagina:
            if pagina >= total_paginas_conhecido:
                print(f"AVISO: Falha na página {pagina}, mas como o limite conhecido era {total_paginas_conhecido}, assumimos o fim da lista.")
                tem_mais = False
            else:
                print(f"AVISO: Não foi possível baixar a página {pagina}. Pulando esta página corrompida da Omie e continuando para a próxima...")
                pagina += 1
                
    return todos_registros


def main():
    print("=== INICIANDO SINCRONIZAÇÃO DE DEPARTAMENTOS ===")
    
    for empresa in EMPRESAS:
        print(f"\nSincronizando departamentos da empresa: {empresa['empresa']}")
        
        departamentos = puxar_departamentos_isolado(empresa)
        
        if departamentos is None:
            print(f"   [!] Erro crítico ao buscar departamentos da {empresa['empresa']}. Pulando empresa.")
            continue
            
        if len(departamentos) == 0:
            print(f"   ℹ Nenhum departamento retornado pela API da Omie para a {empresa['empresa']}.")
            continue
            
        if departamentos:
            print(f"   ✓ {len(departamentos)} departamentos obtidos da Omie. Enviando ao Supabase...")
            
            # Remove os antigos via REST API (para manter o mesmo padrao local)
            try:
                headers_supabase = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal, resolution=merge-duplicates"
                }
                requests.delete(f"{SUPABASE_URL}/rest/v1/departamentos_omie", headers=headers_supabase, params={"empresa_cnpj": f"eq.{empresa['cnpj']}"})
                
                # Insere em lotes
                for i in range(0, len(departamentos), 500):
                    lote = departamentos[i:i+500]
                    for tentativa in range(10):
                        try:
                            # A API supabase oficial python tem dado upsert conflicts, usando REST do main.py
                            resp = requests.post(f"{SUPABASE_URL}/rest/v1/departamentos_omie", json=lote, headers=headers_supabase)
                            if resp.status_code not in (200, 201):
                                raise Exception(f"Erro na API do Supabase: {resp.text}")
                            break
                        except Exception as e:
                            print(f"     [!] Erro ao salvar lote {i} a {i+len(lote)}: {e}. Retentando ({tentativa+1}/10)...")
                            time.sleep(5)
                print(f"   ✅ Departamentos sincronizados com sucesso!")
            except Exception as e:
                print(f"   [X] Erro de rede ao se comunicar com o Supabase: {e}")

    print("\n=== SINCRONIZAÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    main()
