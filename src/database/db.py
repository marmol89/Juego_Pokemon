import os
import sys
import time
from dotenv import load_dotenv
from supabase import create_client, Client
import psycopg2
from urllib.parse import urlparse

# Soporte para ejecutables (PyInstaller)
if getattr(sys, 'frozen', False):
    # Si es un ejecutable, el .env puede estar empaquetado
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    load_dotenv(os.path.join(bundle_dir, '.env'))

# También cargamos del directorio actual por si hay uno externo (sobrescribe lo anterior)
load_dotenv()

class db:

    _client = None

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("\n" + "!"*50)
            print("  CONFIGURACIÓN DE SUPABASE FALTANTE")
            print("!"*50)
            print("  No se ha encontrado el archivo .env o las claves.")
            print("  Por favor, introduce tus credenciales:")
            url = input("  > SUPABASE_URL: ").strip()
            key = input("  > SUPABASE_KEY: ").strip()
            
            if url and key:
                with open(".env", "w") as f:
                    f.write(f"SUPABASE_URL={url}\n")
                    f.write(f"SUPABASE_KEY={key}\n")
                print("\n  [+] Configuración guardada en .env")
                time.sleep(1.5)
            else:
                print("\n  [!] Error: Las credenciales no pueden estar vacías.")
                time.sleep(2)
                return

        if url and key:
            self._client = create_client(url, key)
        
    def get_connection(self) -> Client:
        return self._client

    def _build_pg_connection_string(self) -> str:
        """Build PostgreSQL connection string from env vars."""
        # Try DATABASE_URL first (Supabase connection string format)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return database_url

        # Construct from individual env vars
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if all([host, port, dbname, user, password]):
            return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

        # Fallback: try to parse from SUPABASE_URL
        supabase_url = os.getenv("SUPABASE_URL")
        if supabase_url:
            # Supabase URL format: https://xxxxx.supabase.co
            # Connection string format: postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
            # This is a best-effort fallback - user should set DATABASE_URL for production
            parsed = urlparse(supabase_url)
            # We can't fully construct without the password, but we can provide a hint
            pass

        raise RuntimeError(
            "No database connection configuration found. "
            "Set DATABASE_URL or DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
        )

    def execute_sql(self, sql: str) -> None:
        """Execute raw SQL via psycopg2. Commits on success, rolls back on error."""
        from urllib.parse import urlparse

        conn_str = self._build_pg_connection_string()
        conn = psycopg2.connect(conn_str)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"SQL execution failed: {e}") from e
        finally:
            conn.close()

    def get_tables(self, exclude: list[str] = None) -> list[str]:
        """Query information_schema.tables for public schema tables, excluding provided list."""
        if exclude is None:
            exclude = []

        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name NOT IN (%s)
            ORDER BY table_name
        """
        # Build placeholders for exclude list
        placeholders = ', '.join(['%s'] * len(exclude)) if exclude else 'NULL'

        # We need to dynamically build the query since exclude list varies
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
        if exclude:
            query += f" AND table_name NOT IN ({placeholders})"
        query += " ORDER BY table_name"

        conn_str = self._build_pg_connection_string()
        conn = psycopg2.connect(conn_str)
        try:
            cursor = conn.cursor()
            if exclude:
                cursor.execute(query, exclude)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            conn.close()

    def close(self):
        pass