import os
import pyodbc
import dotenv

# Load environment variables
dotenv.load_dotenv(override=True)

server = os.environ["TPBDD_SERVER"]
database = os.environ["TPBDD_DB"]
username = os.environ["TPBDD_USERNAME"]
password = os.environ["TPBDD_PASSWORD"]
driver = os.environ["ODBC_DRIVER"]

# Connect to the database
conn_str = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

print("Connexion à la base de données...")
with pyodbc.connect(conn_str) as conn:
    cursor = conn.cursor()

    # Get all tables
    print("\n" + "="*80)
    print("TABLES DANS LA BASE DE DONNÉES")
    print("="*80)

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)

    tables = [row.TABLE_NAME for row in cursor.fetchall()]

    for table_name in tables:
        print(f"\n📋 Table: {table_name}")
        print("-" * 80)

        # Get columns for each table
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE,
                   CHARACTER_MAXIMUM_LENGTH, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
        """)

        print(f"{'Colonne':<30} {'Type':<20} {'Nullable':<10} {'Taille':<10}")
        print("-" * 80)

        for col in cursor.fetchall():
            col_name = col.COLUMN_NAME
            data_type = col.DATA_TYPE
            nullable = col.IS_NULLABLE
            max_len = col.CHARACTER_MAXIMUM_LENGTH if col.CHARACTER_MAXIMUM_LENGTH else ''

            print(f"{col_name:<30} {data_type:<20} {nullable:<10} {str(max_len):<10}")

        # Get row count
        cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        row_count = cursor.fetchone().count
        print(f"\n📊 Nombre de lignes: {row_count:,}")

        # Show sample data
        print(f"\n🔍 Exemple de données (5 premières lignes):")
        cursor.execute(f"SELECT TOP 5 * FROM {table_name}")

        columns = [column[0] for column in cursor.description]
        print(f"{' | '.join(columns)}")
        print("-" * 80)

        for row in cursor.fetchall():
            values = [str(v)[:20] if v is not None else 'NULL' for v in row]
            print(f"{' | '.join(values)}")

print("\n" + "="*80)
print("Exploration terminée!")
print("="*80)
