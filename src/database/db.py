import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class db:

    _client = None

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            self._client = create_client(url, key)
        
    def get_connection(self) -> Client:
        return self._client
    
    def close(self):
        pass