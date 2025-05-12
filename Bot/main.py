import openai
from telebot.types import Message

from config_data.config import OPENAI_API_KEY, bot
from dialog_manager import save_dialog, load_dialog_context

openai.api_key = OPENAI_API_KEY

MAX_TELEGRAM_MSG_LENGTH = 4096


def send_long_message(chat_id, text):
    for i in range(0, len(text), MAX_TELEGRAM_MSG_LENGTH):
        bot.send_message(chat_id=chat_id, text=text[i : i + MAX_TELEGRAM_MSG_LENGTH])


@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    bot.reply_to(
        message,
        "Привет!\nЯ ChatGPT-4o Telegram Bot 🤖\nЗадай мне любой вопрос и я постараюсь на него ответить",
    )


@bot.message_handler(commands=["info"])
def bot_info(message: Message):
    bot.reply_to(message, "Используется ChatGPT 4o-mini. Длина контекста 8192 символа.")


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = (
        "Команды:\n" "/start - Начало работы\n" "/help - Справка\n" "/info - Информация\n" "/donate - Поддержать проект"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["donate"])
def bot_donate(message: Message):
    bot.reply_to(message, "Спасибо, что хотите помочь проекту развиваться! Для доната напишите https://t.me/dan4eg")


@bot.message_handler(func=lambda _: True)
def handle_message(message: Message):
    user_id = message.from_user.id
    prompt = message.text

    dialog_id = 'current_dialog_id'
    context = load_dialog_context(user_id, dialog_id)

    messages = []
    for msg in context:
        messages.append({"role": "user", "content": msg['prompt']})
        messages.append({"role": "assistant", "content": msg['response']})
    messages.append({"role": "user", "content": prompt})

    processing_msg = bot.send_message(user_id, "Запрос принят. Обрабатываю...")

    try:
        completion = openai.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.9,
        )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"Ошибка при обращении к OpenAI: {e}"

    try:
        bot.delete_message(chat_id=user_id, message_id=processing_msg.message_id)
    except Exception:
        pass

    save_dialog(user_id, dialog_id, prompt, response)
    send_long_message(chat_id=user_id, text=response)


if __name__ == '__main__':
    bot.infinity_polling()
