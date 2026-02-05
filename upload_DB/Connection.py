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

# ===== 3) 目標表與資料來源 =====
DATA_DIR = Path(r"Z:\Projects\MiC 2026\Data\Time_Difference_csv_6hours")
TABLE_NAME = "TIME_DIFFERENCE"

DB_COLS = ["CALTYPE","CALFORMULA","SOURCE","MESSAGE_NAME","TIMESTAMP","UNIQUE_ID","TRANSACTION_ID","PRIMARY_IDENTIFIER","UNITCOUNT","STAGE_NAME","NEXT_TIME","TIMEDIFF","OLDSTATE_NEWSTATE","LOADFILE"]

# 原始檔欄位 -> DB 欄位（關鍵：補底線 + 修正拼字）
rename_map = {
    # "TIMESTAMP" : "TIMESTAMP",
    # "SOURCE" : "SOURCE",
    # "STAGESEQUENCE" : "STAGE_SEQUENCE",
    # "STAGENAME" : "STAGE_NAME",
    # "STAGETYPE" : "STAGE_TYPE",
    # "LANE" : "LANE",
    # "OLDSTATE" : "OLD_STATE",
    # "OLDSTATEDURATION" : "OLDSTATE_DURATION",
    # "NEWSTATE" : "NEW_STATE",
    # "RELATEDFAULT" : "RELATED_FAULT"
    "CALTYPE": "CALTYPE",
    "CALFORMULA": "CALFORMULA",
    "SOURCE": "SOURCE",
    "MESSAGENAME": "MESSAGE_NAME",
    "TIMESTAMP": "TIMESTAMP",   # 你提到的拼錯版本
    "UNIQUEID": "UNIQUE_ID",
    "TRANSACTIONID": "TRANSACTION_ID",
    "PRIMARYIDENTIFIER": "PRIMARY_IDENTIFIER",
    "UNITCOUNT": "UNITCOUNT",
    "STAGENAME": "STAGE_NAME",
    "NEXTTIME": "NEXT_TIME",
    "TIMEDIFF": "TIMEDIFF", 
    "OLDSTATE-NEWSTATE": "OLDSTATE_NEWSTATE"
}

def already_loaded(loadfile: str) -> bool:
    sql = text(f"SELECT 1 FROM {TABLE_NAME} WHERE LOADFILE = :lf AND ROWNUM = 1")
    with engine.connect() as conn:
        return conn.execute(sql, {"lf": loadfile}).first() is not None

# 將00:00:00格式轉換成秒數
# def duration_to_seconds(series: pd.Series) -> pd.Series:
#     s = series.astype(str).str.strip()
#     s = s.replace({"nan":"", "None":"", "null":"", "(null)":"", "NaT":""})

#     # 把 1.06:02:10 轉成 1 days 06:02:10
#     mask = s.str.match(r"^\d+\.\d{1,2}:\d{2}:\d{2}(\.\d+)?$")
#     s.loc[mask] = s.loc[mask].str.replace(r"^(\d+)\.(.+)$", r"\1 days \2", regex=True)

#     td = pd.to_timedelta(s, errors="coerce")
#     sec = td.dt.total_seconds()

#     # 若本來就是純數字（秒），補上
#     num_sec = pd.to_numeric(s, errors="coerce")
#     sec = sec.fillna(num_sec)

#     return sec  # Float64（含 NA）

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

    # 轉型：時間
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")

    # df["DURATION"] = duration_to_seconds(df["OLDSTATE_DURATION"])

    return df

files = list(DATA_DIR.rglob("*.csv")) + list(DATA_DIR.rglob("*.xlsx")) + list(DATA_DIR.rglob("*.xls"))
if not files:
    print("No files found in:", DATA_DIR)



for fp in files:
    if already_loaded(fp.name):
        print(fp.name, "skip (already loaded)")
        continue

    df = read_one(fp)

    NUM_COLS = ["UNITCOUNT"]  # <- 改成你設為 NUMBER 的兩欄

    for c in NUM_COLS:
        s = df[c].astype(str).str.strip().str.replace(",", "", regex=False)
        # 轉型：轉不過就變 NaN -> 寫入 Oracle 會是 NULL（不會 ORA-01722）
        s = s.replace({"": None, "nan": None, "None": None, "null": None, "(null)": None})
        df[c] = pd.to_numeric(s, errors="coerce")
    
    nat_cnt = int(df["TIMESTAMP"].isna().sum())
    if nat_cnt:
        print(fp.name, f"warning: TIMESTAMP NaT = {nat_cnt}/{len(df)}")

    # LOB_COLS = ["MESSAGECONTENT"]  # 改成你實際的 CLOB 欄位名
    # base_cols = [c for c in df.columns if c not in LOB_COLS]
    # df = df[base_cols + LOB_COLS]
    ordered_cols = ["CALTYPE","CALFORMULA","SOURCE","MESSAGE_NAME","TIMESTAMP","UNIQUE_ID","TRANSACTION_ID","PRIMARY_IDENTIFIER","UNITCOUNT","STAGE_NAME","NEXT_TIME","TIMEDIFF","OLDSTATE_NEWSTATE","LOADFILE"]
    df = df[ordered_cols]

    # keep_sources = {
    # "GKG.GT++-N.GT936MV.C10278.H2-2F-SMT-04H-PRINTER",
    # "GKG.GT++-N.GT935MV.C10279.H2-2F-SMT-04E-PRINTER",
    # "FUJI.M6III.SE0170966-67.C10270.H2-2F-SMT-04H-MOUNTER",
    # "FUJI.M6III.SE0170968.C10272.H2-2F-SMT-04E-MOUNTER"
    # }
    # df = df[df["SOURCE"].isin(keep_sources)]
    
    print("reading:", repr(str(fp)))
    # 舊版 Oracle：不要 method="multi"
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False, chunksize=2000)
    print(fp.name, "uploaded:", len(df))



