import os
import requests
import json
import time
from datetime import datetime, timedelta

# Configurações do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas.")
    exit(1)

SUPABASE_URL = SUPABASE_URL.rstrip('/')

EMPRESAS = [
  { "empresa": "ALIANÇA LEGAL", "cnpj": "12.340.921/0001-82", "app_key": "2901976098021", "app_secret": "e58a09c75425faa713a8e582bcaf29d7" },
  { "empresa": "AUDIT TECNOLOGIA", "cnpj": "44.158.057/0001-99", "app_key": "2790372542958", "app_secret": "e5b71f2190f482fb37aefdf793a124c1" },
  { "empresa": "BRAGA E MONTEIRO", "cnpj": "01.501.108/0001-20", "app_key": "2900573099424", "app_secret": "56b9040a3bc0ebf1af9f393faa048e0d" },
  { "empresa": "E-FISCAL OPERACIONAL", "cnpj": "42.622.192/0001-18", "app_key": "2801550531780", "app_secret": "33cdda263f1bcb7a8ea103e0ef45b8e3" },
  { "empresa": "FERREIRA & MONTEIRO", "cnpj": "56.378.880/0001-99", "app_key": "4552462114200", "app_secret": "2ca77163396e3bd22575f73866d8a009" },
  { "empresa": "GS EDUCAÇÃO", "cnpj": "36.657.397/0001-36", "app_key": "2858651808012", "app_secret": "06a62c592967ba7c20331f486fb735f5" },
  { "empresa": "SF CONSULTORIA", "cnpj": "39.287.808/0001-37", "app_key": "2942348724315", "app_secret": "0c3f0c35957987f78eadaa0ca660e406" },
  { "empresa": "SPACE W", "cnpj": "36.480.461/0001-56", "app_key": "2830369502961", "app_secret": "d7f217ddbc6d383d71611e3c5700878a" },
  { "empresa": "STUDIO ADMINISTRAÇÃO", "cnpj": "27.057.563/0001-72", "app_key": "2830377169620", "app_secret": "9919f8457dfc587e887a7146cf4a1881" },
  { "empresa": "STUDIO AGRONEGÓCIOS", "cnpj": "36.530.240/0001-45", "app_key": "2565363767967", "app_secret": "8d47b5f550f17f730b3f4b4654526965" },
  { "empresa": "STUDIO BANK", "cnpj": "37.852.789/0001-19", "app_key": "2803053196944", "app_secret": "883635355e10841974b7fa858777624b" },
  { "empresa": "STUDIO BROKERS", "cnpj": "14.723.195/0001-02", "app_key": "2565310101354", "app_secret": "0166509939b498522945eb7eb87c9ce9" },
  { "empresa": "STUDIO CONTABILIDADE LTDA", "cnpj": "53.192.862/0001-20", "app_key": "4105288894707", "app_secret": "658c1f268171df853fcc746e2910884d" },
  { "empresa": "STUDIO ENERGY", "cnpj": "34.349.108/0001-06", "app_key": "2565463434534", "app_secret": "00f89766f3241b69815b088798c3931f" },
  { "empresa": "STUDIO FACTORING", "cnpj": "42.275.720/0001-00", "app_key": "2815419517911", "app_secret": "7529bcff39c5e1bcf28ea26124238737" },
  { "empresa": "STUDIO FISCAL", "cnpj": "08.865.854/0001-42", "app_key": "2900565432765", "app_secret": "d409267d73b8886896ffe001c7c93c43" },
  { "empresa": "STUDIO GROWTH", "cnpj": "36.685.910/0001-00", "app_key": "2565409767921", "app_secret": "3e475f5cd987c58f4cf75c97defe25c2" },
  { "empresa": "STUDIO OPERACIONAL", "cnpj": "23.448.109/0001-91", "app_key": "2904360428970", "app_secret": "fbc75836f2a73b196223b5b589306c47" },
  { "empresa": "STUDIO OPERACIONAL 01", "cnpj": "62.700.834/0001-67", "app_key": "6639280694046", "app_secret": "9adcd38ab53ba1a2229d16ca4b333377" },
  { "empresa": "STUDIO PAR", "cnpj": "11.863.345/0001-95", "app_key": "2831312502018", "app_secret": "e4962274b06117e40eca54ca21765a46" },
  { "empresa": "STUDIO FAMILY", "cnpj": "39.349.860/0001-70", "app_key": "2565524767806", "app_secret": "99acd72c4929c99532257067e17ac14d" },
  { "empresa": "STUDIO SBS STORE", "cnpj": "58.420.510/0001-06", "app_key": "5515080151581", "app_secret": "b5d893eb7fcf32e8220d8a4b683f38d6" },
  { "empresa": "STUDIO STORE", "cnpj": "48.552.493/0001-07", "app_key": "3085316581347", "app_secret": "8781fbcaffa8db663e45b6b0af971e52" },
  { "empresa": "STUDIO VAREJO", "cnpj": "44.189.727/0001-34", "app_key": "2751878248119", "app_secret": "3a12157b1f95817bdf58e5e5e37ba994" }
]

def extrair_pagina_omie(url, body):
    for tentativa in range(3):
        try:
            response = requests.post(url, json=body, timeout=30)
            if response.status_code == 200:
                data = response.json()
                registros_pagina = []
                if "clientes_cadastro" in data and len(data["clientes_cadastro"]) > 0:
                    for cliente in data["clientes_cadastro"]:
                        registros_pagina.append(cliente)
                return True, registros_pagina, (data.get("pagina", 1) < data.get("total_de_paginas", 1))
            else:
                print(f"Tentativa {tentativa+1} falhou com status {response.status_code}. Retentando em 5s...")
                time.sleep(5)
        except Exception as e:
            print(f"Tentativa {tentativa+1} falhou com erro: {e}. Retentando em 5s...")
            time.sleep(5)
    return False, [], False

def puxar_clientes_incrementais(empresa_config, data_corte):
    todos_registros_brutos = []
    url = "https://app.omie.com.br/api/v1/geral/clientes/"
    
    # 🚨 Fazemos 4 passagens cruzando Inclusão/Alteração com Inativo S/N
    filtros = [
        {"nome_filtro": "Inclusões (Ativos)", "clientesFiltro": {"dataInclusaoInicial": data_corte, "inativo": "N"}},
        {"nome_filtro": "Inclusões (Inativos)", "clientesFiltro": {"dataInclusaoInicial": data_corte, "inativo": "S"}},
        {"nome_filtro": "Alterações (Ativos)", "clientesFiltro": {"dataAlteracaoInicial": data_corte, "inativo": "N"}},
        {"nome_filtro": "Alterações (Inativos)", "clientesFiltro": {"dataAlteracaoInicial": data_corte, "inativo": "S"}}
    ]

    for f in filtros:
        print(f"  > Buscando {f['nome_filtro']} a partir de {data_corte}...")
        pagina = 1
        tem_mais = True
        
        while tem_mais:
            body = {
                "call": "ListarClientes",
                "app_key": empresa_config["app_key"],
                "app_secret": empresa_config["app_secret"],
                "param": [{
                    "pagina": pagina, 
                    "registros_por_pagina": 100, 
                    "apenas_importado_api": "N",
                    "clientesFiltro": f["clientesFiltro"]
                }]
            }
            
            sucesso, registros_pagina, tem_mais = extrair_pagina_omie(url, body)
            
            if not sucesso:
                print(f"  FALHA CRÍTICA na página {pagina} de {f['nome_filtro']}.")
                return None
                
            todos_registros_brutos.extend(registros_pagina)
            pagina += 1

    # Formatando e limpando duplicatas (pode vir na inclusão e alteração ao mesmo tempo)
    todos_registros = []
    chaves_processadas = set()

    for cliente in todos_registros_brutos:
        pk = cliente.get("codigo_cliente_omie")
        if pk in chaves_processadas:
            continue
        chaves_processadas.add(pk)

        registro = {
            "codigo_cliente_omie": pk,
            "empresa_nome": empresa_config["empresa"],
            "empresa_cnpj": empresa_config["cnpj"],
            "cnpj_cpf": cliente.get("cnpj_cpf"),
            "razao_social": cliente.get("razao_social"),
            "nome_fantasia": cliente.get("nome_fantasia")
        }
        todos_registros.append(registro)
            
    return todos_registros

def rodar_rotina_clientes_incremental():
    data_corte = (datetime.now() - timedelta(days=3)).strftime('%d/%m/%Y')
    
    print(f"Iniciando rotina INCREMENTAL de CLIENTES (A partir de: {data_corte})")
    
    headers_supabase = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal, resolution=merge-duplicates" # UPSERT
    }

    total_processado = 0

    for empresa in EMPRESAS:
        print(f"\nVerificando Deltas de Clientes de: {empresa['empresa']}...")
        clientes = puxar_clientes_incrementais(empresa, data_corte)
        
        if clientes is None:
            print(f"⚠️ ERRO DETECTADO NA EXTRAÇÃO DA {empresa['empresa']}.")
            continue 
            
        if clientes:
            try:
                # 2. Insere/Atualiza os novos dados (NÃO TEM DELETE!)
                tamanho_lote = 500
                for i in range(0, len(clientes), tamanho_lote):
                    lote = clientes[i:i + tamanho_lote]
                    resp = requests.post(f"{SUPABASE_URL}/rest/v1/clientes_grupo", json=lote, headers=headers_supabase)
                    if resp.status_code not in (200, 201):
                         print(f"❌ Erro na API do Supabase (Clientes): {resp.text}")
                
                print(f"✅ UPSERT (Atualizado/Inserido): {len(clientes)} clientes novos/alterados de {empresa['empresa']}")
                total_processado += len(clientes)
            except Exception as e:
                print(f"❌ Erro ao enviar Clientes da empresa {empresa['empresa']}: {e}")
        else:
            print(f"Nenhum cliente novo/alterado para {empresa['empresa']} desde {data_corte}.")

    print(f"\nFIM DA ROTINA INCREMENTAL DE CLIENTES! Total UPSERT: {total_processado} clientes.")

if __name__ == "__main__":
    rodar_rotina_clientes_incremental()
