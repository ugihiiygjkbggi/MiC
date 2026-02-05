from pathlib import Path
import pandas as pd
import oracledb
from sqlalchemy import create_engine, text

# ===== 1) Thick mode =====
oracledb.init_oracle_client(lib_dir=r"C:\NYCU 2527\MiC\Oracle\instantclient_19_29")

# ===== 2) Oracle 連線 =====
USER = "MIC_2026"
PWD  = "2026"
HOST = "140.113.59.168"
PORT = 1521
SID  = "xe"

dsn = oracledb.makedsn(HOST, PORT, sid=SID)
engine = create_engine(f"oracle+oracledb://{USER}:{PWD}@{dsn}")


TABLE_NAME = "PRIMARY_MODEL"
DB_COLS = ["WO_NO","MODEL","LOADFILE"]

# 原始檔欄位 -> DB 欄位（關鍵：補底線 + 修正拼字）
rename_map = {
    "WO NO": "WO_NO",
    "MODEL": "MODEL"
}


def read_one(fp: Path) -> pd.DataFrame:
    df = pd.read_csv(fp) if fp.suffix.lower()==".csv" else pd.read_excel(fp)

    # 先去空白、轉大寫，方便 mapping
    df.columns = [c.strip().upper() for c in df.columns]

    # 欄名對齊到 DB
    df = df.rename(columns=rename_map)

    # 補 LOADFILE
    df["LOADFILE"] = fp.name

    # 補缺欄 + 固定順序
    for c in DB_COLS:
        if c not in df.columns:
            df[c] = pd.NA
    df = df[DB_COLS].copy()

    return df

fp = Path(r"Z:\Projects\MiC 2026\Data\PrimaryModel.csv")
df = read_one(fp)
    # 舊版 Oracle：不要 method="multi"
df.to_sql(TABLE_NAME, engine, if_exists="append", index=False, chunksize=2000)
print(fp.name, "uploaded:", len(df))



