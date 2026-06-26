from pathlib import Path
from itsdangerous import Serializer, URLSafeTimedSerializer

from app.config import security_settings

App_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = App_DIR.joinpath("template")
