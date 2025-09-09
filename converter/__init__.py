from converter.components.auth_manager import AuthManager
from dotenv import load_dotenv

load_dotenv()

auth_provider = AuthManager("pybritive").auth_provider
