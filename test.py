from dotenv import load_dotenv
import os
load_dotenv()  # This will load the variables fr
print(os.getenv('SUPABASE_URL'))