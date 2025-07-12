# Load OpenAI API key from a secret file
OPENAI_API_KEY = None
secret_path = os.path.join(os.path.dirname(__file__), '..', 'openai_api_key.secret')
try:
    with open(secret_path, 'r') as f:
        OPENAI_API_KEY = f.read().strip()
except FileNotFoundError:
    OPENAI_API_KEY = None