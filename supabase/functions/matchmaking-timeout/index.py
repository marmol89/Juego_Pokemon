"""
Edge Function: matchmaking-timeout
Cron job that runs every 30s to clean up expired queue entries.
Marks entries as 'timeout' if they've been waiting for 60+ seconds.
"""
import os
import json
from supabase import create_client, Client
from psycopg2 import connect


def get_db_connection():
    """Get PostgreSQL connection from environment."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return connect(database_url)
    
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    
    if all([host, port, dbname, user, password]):
        return connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
    
    raise RuntimeError("No database connection configuration found")


def handler(req: dict) -> dict:
    """
    Cron handler - runs every 30s.
    Finds expired 'waiting' entries, marks them as timeout, deletes them,
    and broadcasts timeout event to each user.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find expired entries
        cursor.execute(
            """
            SELECT id, user_id, rating, rating_diff_max, status, room_id, entered_at, updated_at
            FROM matchmaking_queue
            WHERE status = 'waiting'
              AND entered_at < now() - interval '60 seconds'
            """
        )
        expired_rows = cursor.fetchall()
        
        if not expired_rows:
            return {"status": "ok", "processed": 0}
        
        processed = 0
        for row in expired_rows:
            user_id = row[1]
            
            # Mark as timeout
            cursor.execute(
                """
                UPDATE matchmaking_queue
                SET status = 'timeout'
                WHERE user_id = %s AND status = 'waiting'
                """,
                (user_id,)
            )
            
            # Delete the entry
            cursor.execute(
                "DELETE FROM matchmaking_queue WHERE user_id = %s",
                (user_id,)
            )
            
            conn.commit()
            processed += 1
            
            # Broadcast timeout event
            broadcast_timeout(user_id)
        
        cursor.close()
        conn.close()
        
        return {"status": "ok", "processed": processed}
        
    except Exception as e:
        print(f"[matchmaking-timeout] Error: {e}")
        return {"status": "error", "message": str(e)}


def broadcast_timeout(user_id: str):
    """Broadcast timeout event to user via Supabase Realtime."""
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print(f"[matchmaking-timeout] Supabase credentials not found for user {user_id}")
            return
        
        client: Client = create_client(supabase_url, supabase_key)
        
        channel = client.channel(f"matchmaking:{user_id}")
        channel.on_event("broadcast", lambda e: None)
        channel.subscribe()
        channel.send_broadcast(
            event="matchmaking_timeout",
            payload={}
        )
        
    except Exception as e:
        print(f"[matchmaking-timeout] Realtime broadcast error for {user_id}: {e}")


# Supabase Edge Function entry point
def main(req: dict):
    return handler(req)


if __name__ == "__main__":
    print(handler({}))
