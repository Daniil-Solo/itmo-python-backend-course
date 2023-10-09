import os
from dotenv import load_dotenv


load_dotenv()
TEST_MODE = os.environ["MODE"] == "TEST"
DB_FILEPATH = os.environ['DB_FILEPATH']
if TEST_MODE:
    # тестируем в оперативной памяти
    DB_URL = "sqlite+aiosqlite:///:memory:"
else:
    DB_URL = f"sqlite+aiosqlite:///{os.environ['DB_FILEPATH']}"
