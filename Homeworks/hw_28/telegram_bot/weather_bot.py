import os
import aiohttp
import time
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from logger import logger


# ---- Load Environment Variables ----
load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
API_KEY = os.getenv('API_KEY')

if not TG_TOKEN:
    logger.critical("TG_TOKEN not found in environment variables.")
    raise ValueError("No TG_TOKEN found in environment variables.")
if not API_KEY:
    logger.critical("API_KEY not found in environment variables.")
    raise ValueError("No API_KEY found in environment variables.")


# ---- Define Asynchronous Weather Function ----
async def get_weather_async(city: str) -> str:
    """
    Fetch weather information for a given city asynchronously.

    :param city: Name of the city to fetch weather for.
    :type city: str
    :return: A formatted string with weather details or an error message.
    :rtype: str
    """
    start_time = time.time()
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Successful API request for city: {city} in {execution_time:.2f} seconds")

        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        return (
            f"🌤 Weather in {city.title()}:\n"
            f"🔹 Currently: {weather_description}\n"
            f"🌡 Temperature: {temperature} °C\n"
            f"🌡 Feels like: {feels_like} °C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🔻 Pressure: {pressure} hPa"
        )

    except aiohttp.ClientResponseError as http_err:
        end_time = time.time()
        execution_time = end_time - start_time
        logger.error(f"HTTP error for city '{city}' in {execution_time:.2f} seconds: {http_err}")
        return f"Sorry, I couldn't find weather information for '{city}'. Please check the city name and try again."

    except Exception as err:
        end_time = time.time()
        execution_time = end_time - start_time
        logger.error(f"Error fetching weather for city '{city}' in {execution_time:.2f} seconds: {err}")
        return f"An unexpected error occurred. Please try again later."


# ---- Define Bot Command Handlers ----
async def handle_city(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming messages with city names and respond with weather details.

    :param update: Telegram update object containing message data.
    :type update: telegram.ext.Updater
    :param context: Telegram context object.
    :type context: telegram.ext.CallbackContext
    """
    city = update.message.text.strip()
    user_id = update.effective_user.id
    logger.info(f"Received weather request for city: {city} from user {user_id}")
    weather_info = await get_weather_async(city)
    await update.message.reply_text(weather_info)


async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    """
    Respond to the /start command with a greeting message.

    :param update: Telegram update object.
    :type update: telegram.ext.Updater
    :param context: Telegram context object.
    :type context: telegram.ext.CallbackContext
    """
    await update.message.reply_text(
        "Hello! I am a weather bot.\n"
        "Enter the name of a city to get the weather.\n"
        "For example: London"
    )
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started the bot.")


async def ask_help(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    """
    Respond to the /help command with usage instructions.

    :param update: Telegram update object.
    :type update: telegram.ext.Updater
    :param context: Telegram context object.
    :type context: telegram.ext.CallbackContext
    """
    await update.message.reply_text(
        "Bot accepts city names in English or Ukrainian languages.\n"
        "Simply enter city's name to get a current weather."
    )


# ---- Main Function for Bot Initialization ----
def main():
    """
    Initialize and run the Telegram bot.

    :return: None
    """
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', ask_help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city))

    logger.info("Bot started polling.")
    application.run_polling()


if __name__ == '__main__':
    main()
