from pathlib import Path
import pandas as pd
import numpy as np

# =========================
# CONFIGURACIÓN
# =========================

KEY = "ffm_subscriber_id"

CRITICAL_FIELDS = [
    "plan_hios_id",
    "policy_status",
    "subsidy",
    "net_premium",
    "effective_date"
]

BASE_DIR = Path(__file__).resolve().parents[3]


# =========================
# UTILIDADES
# =========================

def standardize_columns(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def normalize_data(df):
    df = df.copy()

    # Normalizar texto general
    for col in df.columns:
        df.loc[:, col] = df[col].astype(str).str.strip()

    # Normalizar numéricos importantes
    for col in ["subsidy", "net_premium"]:
        if col in df.columns:
            df.loc[:, col] = (
                df[col]
                .str.replace(r"[^0-9.-]", "", regex=True)
                .replace("", np.nan)
                .astype(float)
            )

    return df


# =========================
# CARGA DE ARCHIVOS
# =========================

def load_files():

    mp_path = BASE_DIR / "src" / "cleaning" / "mp_clean_file.csv"
    crm_path = BASE_DIR / "src" / "cleaning" / "crm_clean_file.csv"

    print("Loading MP:", mp_path) 
    print("Loading CRM:", crm_path)

    mp = pd.read_csv(mp_path)
    crm = pd.read_csv(crm_path)

    # Estandarizar nombres de columnas
    mp = standardize_columns(mp)
    crm = standardize_columns(crm)

    # Renombrar llave en CRM
    if "mp_id" in crm.columns:
        crm = crm.rename(columns={"mp_id": KEY})

    # Validar existencia de llave
    if KEY not in mp.columns:
        raise ValueError(f"{KEY} no existe en MP")

    if KEY not in crm.columns:
        raise ValueError(f"{KEY} no existe en CRM")

    return mp, crm


# =========================
# COMPARACIÓN
# =========================

def compare_datasets(mp, crm):

    mp = normalize_data(mp)
    crm = normalize_data(crm)

    merged = mp.merge(
        crm,
        on=KEY,
        how="outer",
        suffixes=("_mp", "_crm"),
        indicator=True
    )

    new_records = merged[merged["_merge"] == "left_only"]
    missing_records = merged[merged["_merge"] == "right_only"]
    common = merged[merged["_merge"] == "both"]

    return merged, new_records, missing_records, common


# =========================
# AUDITORÍA CRÍTICA
# =========================

def detect_critical_changes(common_df):

    audit_results = []

    for field in CRITICAL_FIELDS:

        mp_col = f"{field}_mp"
        crm_col = f"{field}_crm"

        if mp_col not in common_df.columns:
            continue

        diff = common_df[
            common_df[mp_col].fillna("") != common_df[crm_col].fillna("")
        ]

        if not diff.empty:
            temp = diff[[KEY, mp_col, crm_col]].copy()
            temp["changed_field"] = field
            audit_results.append(temp)

    if audit_results:
        return pd.concat(audit_results, ignore_index=True)

    return pd.DataFrame()


# =========================
# RESUMEN
# =========================

def generate_summary(new_records, missing_records, changes):

    print("\n========== AUDITORÍA MARKETPLACE ==========")
    print("Nuevos en Marketplace:", len(new_records))
    print("Cancelados o faltantes en MP:", len(missing_records))
    print("Registros con cambios críticos:", changes[KEY].nunique())

    if not changes.empty:
        print("\nDetalle cambios por tipo:")
        print(changes["changed_field"].value_counts())

    print("===========================================\n")


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    mp, crm = load_files()

    merged, new_records, missing_records, common = compare_datasets(mp, crm)

    changes = detect_critical_changes(common)

    generate_summary(new_records, missing_records, changes)

    # Exportar reportes
    output_dir = BASE_DIR / "data" / "audits"
    output_dir.mkdir(exist_ok=True)

    new_records.to_csv(output_dir / "audit_new_records.csv", index=False)
    missing_records.to_csv(output_dir / "audit_missing_records.csv", index=False)
    changes.to_csv(output_dir / "audit_critical_changes.csv", index=False)

    print("Archivos de auditoría generados en:", output_dir)