import os
from dotenv import load_dotenv

# Carrega variáveis
load_dotenv("C:/Users/cristhofer.maciel.GRUPOSTUDIO/Grupo_Studio/omie-supabase-etl/.env")

import conta_corrente_etl

if __name__ == "__main__":
    conta_corrente_etl.rodar_rotina_cc()
