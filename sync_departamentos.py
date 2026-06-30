import os
import requests
import time
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: Variáveis de ambiente SUPABASE_URL ou SUPABASE_KEY não configuradas.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TODAS_EMPRESAS = [
    {"empresa": "ALIANÇA LEGAL", "app_key": "2901976098021", "app_secret": "e58a09c75425faa713a8e582bcaf29d7", "cnpj": "12.340.921/0001-82"},
    {"empresa": "AUDIT TECNOLOGIA", "app_key": "2790372542958", "app_secret": "e5b71f2190f482fb37aefdf793a124c1", "cnpj": "44.158.057/0001-99"},
    {"empresa": "BRAGA E MONTEIRO", "app_key": "2900573099424", "app_secret": "56b9040a3bc0ebf1af9f393faa048e0d", "cnpj": "01.501.108/0001-20"},
    {"empresa": "E-FISCAL OPERACIONAL", "app_key": "2801550531780", "app_secret": "33cdda263f1bcb7a8ea103e0ef45b8e3", "cnpj": "42.622.192/0001-18"},
    {"empresa": "FERREIRA & MONTEIRO", "app_key": "4552462114200", "app_secret": "2ca77163396e3bd22575f73866d8a009", "cnpj": "56.378.880/0001-99"},
    {"empresa": "GS EDUCAÇÃO", "app_key": "2858651808012", "app_secret": "06a62c592967ba7c20331f486fb735f5", "cnpj": "36.657.397/0001-36"},
    {"empresa": "SF CONSULTORIA", "app_key": "2942348724315", "app_secret": "0c3f0c35957987f78eadaa0ca660e406", "cnpj": "39.287.808/0001-37"},
    {"empresa": "SPACE W", "app_key": "2830369502961", "app_secret": "d7f217ddbc6d383d71611e3c5700878a", "cnpj": "36.480.461/0001-56"},
    {"empresa": "STUDIO ADMINISTRAÇÃO", "app_key": "2830377169620", "app_secret": "9919f8457dfc587e887a7146cf4a1881", "cnpj": "27.057.563/0001-72"},
    {"empresa": "STUDIO AGRONEGÓCIOS", "app_key": "2565363767967", "app_secret": "8d47b5f550f17f730b3f4b4654526965", "cnpj": "36.530.240/0001-45"},
    {"empresa": "STUDIO BANK", "app_key": "2803053196944", "app_secret": "883635355e10841974b7fa858777624b", "cnpj": "37.852.789/0001-19"},
    {"empresa": "STUDIO BROKERS", "app_key": "2565310101354", "app_secret": "0166509939b498522945eb7eb87c9ce9", "cnpj": "14.723.195/0001-02"},
    {"empresa": "STUDIO CONTABILIDADE LTDA", "app_key": "4105288894707", "app_secret": "658c1f268171df853fcc746e2910884d", "cnpj": "53.192.862/0001-20"},
    {"empresa": "STUDIO ENERGY", "app_key": "2565463434534", "app_secret": "00f89766f3241b69815b088798c3931f", "cnpj": "34.349.108/0001-06"},
    {"empresa": "STUDIO FACTORING", "app_key": "2815419517911", "app_secret": "7529bcff39c5e1bcf28ea26124238737", "cnpj": "42.275.720/0001-00"},
    {"empresa": "STUDIO FISCAL", "app_key": "2900565432765", "app_secret": "d409267d73b8886896ffe001c7c93c43", "cnpj": "08.865.854/0001-42"},
    {"empresa": "STUDIO GROWTH", "app_key": "2565409767921", "app_secret": "3e475f5cd987c58f4cf75c97defe25c2", "cnpj": "36.685.910/0001-00"},
    {"empresa": "STUDIO OPERACIONAL", "app_key": "2904360428970", "app_secret": "fbc75836f2a73b196223b5b589306c47", "cnpj": "23.448.109/0001-91"},
    {"empresa": "STUDIO OPERACIONAL 01", "app_key": "6639280694046", "app_secret": "9adcd38ab53ba1a2229d16ca4b333377", "cnpj": "62.700.834/0001-67"},
    {"empresa": "STUDIO PAR", "app_key": "2831312502018", "app_secret": "e4962274b06117e40eca54ca21765a46", "cnpj": "11.863.345/0001-95"},
    {"empresa": "STUDIO FAMILY", "app_key": "2565524767806", "app_secret": "99acd72c4929c99532257067e17ac14d", "cnpj": "39.349.860/0001-70"},
    {"empresa": "STUDIO SBS STORE", "app_key": "5515080151581", "app_secret": "b5d893eb7fcf32e8220d8a4b683f38d6", "cnpj": "58.420.510/0001-06"},
    {"empresa": "STUDIO STORE", "app_key": "3085316581347", "app_secret": "8781fbcaffa8db663e45b6b0af971e52", "cnpj": "48.552.493/0001-07"},
    {"empresa": "STUDIO VAREJO", "app_key": "2751878248119", "app_secret": "3a12157b1f95817bdf58e5e5e37ba994", "cnpj": "44.189.727/0001-34"}
]

def formatar_registro(dept, empresa_config):
    return {
        "codigo": dept.get("codigo"),
        "empresa_nome": empresa_config["empresa"],
        "empresa_cnpj": empresa_config["cnpj"],
        "descricao": dept.get("descricao"),
        "estrutura": dept.get("estrutura"),
        "inativo": dept.get("inativo")
    }

def tentar_pagina(url, empresa_config, pagina, tamanho, max_tentativas=10):
    """Tenta baixar uma página específica da Omie com retries."""
    body = {
        "call": "ListarDepartamentos",
        "app_key": empresa_config["app_key"],
        "app_secret": empresa_config["app_secret"],
        "param": [{"pagina": pagina, "registros_por_pagina": tamanho}]
    }
    for tentativa in range(max_tentativas):
        try:
            response = requests.post(url, json=body, timeout=30)
            if response.status_code == 200:
                data = response.json()
                total_paginas = data.get("total_de_paginas", 1)
                registros = []
                if "departamentos" in data and len(data["departamentos"]) > 0:
                    registros = data["departamentos"]
                return True, registros, total_paginas
            else:
                print(f"    Tentativa {tentativa+1} falhou na página {pagina} (tamanho {tamanho}) com status {response.status_code}. Retentando em 5s...")
                time.sleep(5)
        except Exception as e:
            print(f"    Tentativa {tentativa+1} falhou na página {pagina} (tamanho {tamanho}) com erro: {e}. Retentando em 5s...")
            time.sleep(5)
    return False, [], 0

def zoom_progressivo(url, empresa_config, pagina_falha, tamanho_original):
    """Quando uma página falha, divide em lotes menores para isolar o registro corrompido e resgatar os bons."""
    registros_recuperados = []
    tamanho_zoom1 = 10
    fator = tamanho_original // tamanho_zoom1
    pag_inicio = (pagina_falha - 1) * fator + 1
    pag_fim = pagina_falha * fator
    
    print(f"  🔬 ZOOM NÍVEL 1: Tentando recuperar página {pagina_falha} como sub-páginas {pag_inicio}-{pag_fim} (de {tamanho_zoom1} registros)...")
    
    for sub_pag in range(pag_inicio, pag_fim + 1):
        sucesso, registros, _ = tentar_pagina(url, empresa_config, sub_pag, tamanho_zoom1, max_tentativas=5)
        if sucesso:
            registros_recuperados.extend(registros)
            print(f"    ✅ Sub-página {sub_pag}: {len(registros)} departamentos recuperados")
        else:
            tamanho_zoom2 = 1
            fator2 = tamanho_zoom1 // tamanho_zoom2
            micro_inicio = (sub_pag - 1) * fator2 + 1
            micro_fim = sub_pag * fator2
            
            print(f"    🔬 ZOOM NÍVEL 2: Tentando sub-página {sub_pag} como micro-páginas {micro_inicio}-{micro_fim} (1 dept cada)...")
            
            for micro_pag in range(micro_inicio, micro_fim + 1):
                ok, regs, _ = tentar_pagina(url, empresa_config, micro_pag, tamanho_zoom2, max_tentativas=3)
                if ok:
                    registros_recuperados.extend(regs)
                else:
                    print(f"      ❌ Micro-página {micro_pag}: departamento irrecuperável (defeito na Omie)")
    return registros_recuperados

def puxar_departamentos_isolado(empresa_config):
    TAMANHO_PAGINA = 50
    pagina = 1
    tem_mais = True
    total_paginas_conhecido = 999999
    todos_registros_brutos = []
    url = "https://app.omie.com.br/api/v1/geral/departamentos/"
    
    while tem_mais:
        sucesso, registros_pagina, total_paginas = tentar_pagina(url, empresa_config, pagina, TAMANHO_PAGINA)
        
        if sucesso:
            total_paginas_conhecido = total_paginas
            todos_registros_brutos.extend(registros_pagina)
            
            if pagina >= total_paginas_conhecido:
                tem_mais = False
            else:
                pagina += 1
        else:
            if pagina >= total_paginas_conhecido:
                print(f"  AVISO: Falha na página {pagina}, mas já atingimos o limite ({total_paginas_conhecido}). Encerrando.")
                tem_mais = False
            else:
                print(f"  ⚠️ Página {pagina} falhou! Ativando Zoom Progressivo...")
                registros_zoom = zoom_progressivo(url, empresa_config, pagina, TAMANHO_PAGINA)
                todos_registros_brutos.extend(registros_zoom)
                print(f"  🔬 Zoom recuperou {len(registros_zoom)} de {TAMANHO_PAGINA} departamentos da página {pagina}")
                pagina += 1
                
    todos_registros = []
    chaves_processadas = set()
    for dept in todos_registros_brutos:
        pk = dept.get("codigo")
        if pk in chaves_processadas:
            continue
        chaves_processadas.add(pk)
        todos_registros.append(formatar_registro(dept, empresa_config))
        
    return todos_registros

def main(empresa_alvo=None):
    print("=== INICIANDO SINCRONIZAÇÃO DE DEPARTAMENTOS ===")
    
    empresas_para_rodar = TODAS_EMPRESAS
    if empresa_alvo:
        empresas_para_rodar = [e for e in TODAS_EMPRESAS if e["empresa"] == empresa_alvo]
        if not empresas_para_rodar:
            print(f"ERRO: Empresa '{empresa_alvo}' não encontrada na lista.")
            return

    for empresa in empresas_para_rodar:
        print(f"\nSincronizando departamentos da empresa: {empresa['empresa']}")
        
        departamentos = puxar_departamentos_isolado(empresa)
        
        if departamentos is None:
            print(f"   [!] Erro crítico ao buscar departamentos da {empresa['empresa']}. Pulando empresa.")
            continue
            
        if len(departamentos) == 0:
            print(f"   ℹ Nenhum departamento retornado pela API da Omie para a {empresa['empresa']}.")
            continue
            
        if departamentos:
            print(f"   ✓ {len(departamentos)} departamentos obtidos da Omie. Enviando ao Supabase (UPSERT)...")
            
            try:
                headers_supabase = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal, resolution=merge-duplicates" # UPSERT
                }
                
                # Insere em lotes
                for i in range(0, len(departamentos), 500):
                    lote = departamentos[i:i+500]
                    for tentativa in range(10):
                        try:
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
    if len(sys.argv) > 1:
        empresa_cli = sys.argv[1]
        main(empresa_cli)
    else:
        main()
