#!/usr/bin/env python3
"""
Migration & Seeder CLI for Juego_Pokemon

Usage:
    python migrate.py --migrate   # Run pending migrations
    python migrate.py --reset     # Drop all tables (except _migrations), re-migrate
    python migrate.py --reseed    # reset + run seed scripts
"""
import argparse
import os
import sys
import glob
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from database.db import db

load_dotenv()


def _get_applied_migrations(database):
    """Get list of applied migration names from _migrations table."""
    import psycopg2
    conn_str = database._build_pg_connection_string()
    conn = psycopg2.connect(conn_str)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM _migrations")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()


def _mark_migration_applied(database, name):
    """Record a migration as applied."""
    import psycopg2
    conn_str = database._build_pg_connection_string()
    conn = psycopg2.connect(conn_str)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO _migrations (name) VALUES (%s)", (name,))
        conn.commit()
    finally:
        conn.close()


def list_migrations():
    """Reads migrations/*.sql, sorts lexicographically, returns list of (filename, filepath)."""
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    pattern = os.path.join(migrations_dir, '*.sql')
    files = glob.glob(pattern)
    # Sort lexicographically
    sorted_files = sorted(files)
    return [(os.path.basename(f), f) for f in sorted_files]


def run_migrate():
    """Execute --migrate flow."""
    database = db()
    migrations = list_migrations()

    if not migrations:
        print("No migration files found.")
        return

    try:
        applied_migrations = _get_applied_migrations(database)
    except Exception:
        # Table might not exist yet - start fresh
        applied_migrations = []

    unapplied = []
    for filename, filepath in migrations:
        if filename not in applied_migrations:
            unapplied.append((filename, filepath))

    if not unapplied:
        print("No new migrations to apply.")
        print("Applied 0 migrations")
        return

    for filename, filepath in unapplied:
        print(f"Applying migration: {filename}")
        with open(filepath, 'r') as f:
            sql = f.read()
        database.execute_sql(sql)
        _mark_migration_applied(database, filename)

    print(f"Applied {len(unapplied)} migrations")


def run_reset():
    """Execute --reset flow."""
    print("This will DROP ALL TABLES. Type 'yes' to confirm: ")
    confirmation = input().strip()
    if confirmation != 'yes':
        print("Reset aborted.")
        sys.exit(1)

    database = db()

    # Get tables excluding _migrations
    tables = database.get_tables(exclude=['_migrations'])

    # Safe drop order based on FK dependencies:
    # battles -> rooms -> teams -> movements -> user_items -> users -> pokemons -> items
    safe_order = ['battles', 'movements', 'teams', 'rooms', 'user_items', 'users', 'pokemons', 'items']

    # Only drop tables that exist
    for table in safe_order:
        if table in tables:
            print(f"Dropping table: {table}")
            database.execute_sql(f"DROP TABLE IF EXISTS {table} CASCADE")

    # Clear _migrations so migrations re-run after reset
    database.execute_sql("TRUNCATE TABLE _migrations")

    print("Reset complete")
    print("Running migrations...")
    run_migrate()


def run_reseed():
    """Execute --reseed flow."""
    run_reset()

    print("Seeding pokemons...")
    result = os.system(f'"{sys.executable}" src/scripts/seed_pokemons.py')
    if result != 0:
        print("Warning: seed_pokemons.py returned non-zero exit code")

    print("Seeding items...")
    result = os.system(f'"{sys.executable}" src/scripts/seed_items.py')
    if result != 0:
        print("Warning: seed_items.py returned non-zero exit code")

    print("Reseed complete")


def main():
    parser = argparse.ArgumentParser(description='Migration & Seeder CLI')
    parser.add_argument('--migrate', action='store_true', help='Run pending migrations')
    parser.add_argument('--reset', action='store_true', help='Drop all tables and re-migrate')
    parser.add_argument('--reseed', action='store_true', help='Reset tables, re-migrate, and run seeders')

    args = parser.parse_args()

    if args.migrate:
        run_migrate()
        sys.exit(0)
    elif args.reset:
        run_reset()
        sys.exit(0)
    elif args.reseed:
        run_reseed()
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
