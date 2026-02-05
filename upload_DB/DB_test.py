import oracledb
from sqlalchemy import create_engine, text

# 指到你解壓的 instant client 資料夾（有 oci.dll 的那層）
oracledb.init_oracle_client(lib_dir=r"C:\NYCU 2527\MiC\Oracle\instantclient_19_29")

USER = "MIC_2026"
PWD  = "2026"
HOST = "140.113.59.168"
PORT = 1521

dsn = oracledb.makedsn(HOST, PORT, sid="xe")  # 你 SQL Developer 用 SID=xe
engine = create_engine(f"oracle+oracledb://{USER}:{PWD}@{dsn}")

with engine.connect() as conn:
    print(conn.execute(text("SELECT 1 FROM dual")).scalar())
