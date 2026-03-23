import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("DEBUG → SUPABASE_URL:", SUPABASE_URL)
print("DEBUG → SUPABASE_SERVICE_ROLE_KEY:", SUPABASE_SERVICE_ROLE_KEY)

supabase = None

def init_supabase():
    global supabase

    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        print("Supabase credentials not set. Skipping Supabase initialization.")
        return None

    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        print("Supabase initialized successfully.")
        return supabase
    except Exception as e:
        print(f"Supabase initialization failed: {e}")
        supabase = None
        return None


# Initialize safely (will not crash app)
init_supabase()