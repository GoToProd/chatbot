import logging
import os

import openai
import telebot
from dotenv import load_dotenv
from telebot import StateMemoryStorage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("info", "Справка по работе"),
    ("donate", "Справка по работе"),
)

storage = StateMemoryStorage()

bot = telebot.TeleBot(BOT_TOKEN, state_storage=storage)

log_dir = os.path.join(os.path.dirname(__file__), "ChatGPT_Logs")
ch = logging.StreamHandler()
logger = logging.getLogger(__name__)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=os.path.join(log_dir, "error.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
