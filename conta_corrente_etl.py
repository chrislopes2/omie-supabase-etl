import os
import requests
import json
from datetime import datetime

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

def converter_data(data_br):
    if not data_br:
        return None
    try:
        partes = data_br.split('/')
        return f"{partes[2]}-{partes[1]}-{partes[0]}"
    except:
        return None

def converter_data_hora(data_br, hora_br):
    if not data_br or not hora_br:
        return None
    try:
        data_fmt = converter_data(data_br)
        return f"{data_fmt}T{hora_br}Z"
    except:
        return None

def puxar_conta_corrente(empresa_config):
    pagina = 1
    tem_mais = True
    todos_registros = []
    url = "https://app.omie.com.br/api/v1/financas/contacorrentelancamentos/"
    
    while tem_mais:
        body = {
            "call": "ListarLancCC",
            "app_key": empresa_config["app_key"],
            "app_secret": empresa_config["app_secret"],
            "param": [{"nPagina": pagina, "nRegPorPagina": 100}]
        }
        response = requests.post(url, json=body)
        if response.status_code != 200:
            break
            
        data = response.json()
        if "listaLancamentos" in data and len(data["listaLancamentos"]) > 0:
            for lanc in data["listaLancamentos"]:
                cabecalho = lanc.get("cabecalho", {})
                detalhes = lanc.get("detalhes", {})
                diversos = lanc.get("diversos", {})
                info = lanc.get("info", {})
                
                registro = {
                    "codigo_lancamento": lanc.get("nCodLanc"),
                    "empresa_nome": empresa_config["empresa"],
                    "empresa_cnpj": empresa_config["cnpj"],
                    "id_conta_corrente": cabecalho.get("nCodCC"),
                    "data_lancamento": converter_data(cabecalho.get("dDtLanc")),
                    "valor": cabecalho.get("nValorLanc"),
                    "codigo_categoria": detalhes.get("cCodCateg"),
                    "numero_documento": detalhes.get("cNumDoc"),
                    "tipo_documento": detalhes.get("cTipo"),
                    "observacao": detalhes.get("cObs"),
                    "id_cliente_fornecedor": detalhes.get("nCodCliente"),
                    "id_projeto": detalhes.get("nCodProjeto"),
                    "natureza": diversos.get("cNatureza"),
                    "origem": diversos.get("cOrigem"),
                    "data_conciliacao": converter_data(diversos.get("dDtConc")),
                    "data_inclusao": converter_data(info.get("dInc")),
                    "usuario_inclusao": info.get("uInc"),
                    "last_update": converter_data_hora(info.get("dAlt"), info.get("hAlt")),
                    "departamentos": lanc.get("departamentos"),
                    "id_origem_receber": diversos.get("nCodLancCR", None),
                    "id_origem_pagar": diversos.get("nCodLancCP", None)
                }
                todos_registros.append(registro)
            pagina += 1
        else:
            tem_mais = False
            
    return todos_registros

def rodar_rotina_cc():
    print("Iniciando rotina de Conta Corrente (Multi-Tenant Omie -> Supabase)...")
    
    headers_supabase = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal, resolution=merge-duplicates"
    }

    print("Limpando base de dados antiga de conta_corrente no Supabase...")
    try:
        requests.delete(f"{SUPABASE_URL}/rest/v1/conta_corrente?codigo_lancamento=gt.0", headers=headers_supabase)
        print("Tabela conta_corrente limpa com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar tabela conta_corrente: {e}")

    for empresa in EMPRESAS:
        print(f"\nExtraindo Conta Corrente de: {empresa['empresa']}...")
        lancamentos_cc = puxar_conta_corrente(empresa)
        if lancamentos_cc:
            try:
                tamanho_lote = 500
                for i in range(0, len(lancamentos_cc), tamanho_lote):
                    lote = lancamentos_cc[i:i + tamanho_lote]
                    resp = requests.post(f"{SUPABASE_URL}/rest/v1/conta_corrente", json=lote, headers=headers_supabase)
                    if resp.status_code not in (200, 201):
                         print(f"❌ Erro na API do Supabase (Conta Corrente): {resp.text}")
                print(f"✅ Inseridos {len(lancamentos_cc)} Lançamentos CC para {empresa['empresa']}")
            except Exception as e:
                print(f"❌ Erro ao enviar Conta Corrente da empresa {empresa['empresa']}: {e}")

    print("\nFIM DA ROTINA DE CONTA CORRENTE!")

if __name__ == "__main__":
    rodar_rotina_cc()
