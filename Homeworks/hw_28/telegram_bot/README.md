# Telegram Weather Bot

A Telegram bot that provides real-time weather information for any city using the OpenWeatherMap API. The bot is designed to run continuously, leveraging robust logging mechanisms to monitor its operations effectively.

## Table of Contents

- [Features](#features)
- [APIs Used](#apis-used)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment (Optional but Recommended)](#2-create-a-virtual-environment-optional-but-recommended)
  - [3. Install Dependencies](#3-install-dependencies)
- [Setup](#setup)
  - [1. Obtain API Keys](#1-obtain-api-keys)
  - [2. Create a .env File](#2-create-a-env-file)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
- [Example](#example)
  - [User Interaction](#user-interaction)
- [Logging](#logging)
  - [Log File Rotation](#log-file-rotation)
  - [Accessing Logs](#accessing-logs)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-Time Weather Data:** Provides current weather information including temperature, humidity, pressure, and more.
- **User-Friendly Interface:** Simple commands and clear responses make it easy to use.
- **Robust Logging:** Implements log file rotation to manage log sizes and maintain backup logs.
- **Secure Configuration:** Utilizes environment variables to protect sensitive information.

## APIs Used

- **Telegram Bot API:** Enables interaction with Telegram users.
- **OpenWeatherMap API:** Provides comprehensive weather data for any location worldwide.

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/telegram-weather-bot.git
cd telegram-weather-bot
```

### 2. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment ensures that your project dependencies are isolated from other projects.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

**Note:** Ensure that your `requirements.txt` includes the following packages:

```text
aiohttp==3.11.11
python-dotenv==1.0.1
python-telegram-bot==21.9
requests==2.32.3
certifi==2024.12.14
```

## Setup

### 1. Obtain API Keys

#### Telegram Bot Token
- Open Telegram and search for @BotFather.
- Start a conversation and send the `/newbot` command.
- Follow the prompts to set up your bot. You'll receive a Telegram Bot Token (`TG_TOKEN`), which looks like `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ`.

#### OpenWeatherMap API Key
- Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/).
- Navigate to the API keys section in your account dashboard.
- Generate a new API Key (`API_KEY`).

### 2. Create a .env File

Create a `.env` file in the root directory of your project to store your environment variables securely.

```env
TG_TOKEN=your_telegram_bot_token_here
API_KEY=your_openweathermap_api_key_here
```

**Security Tip:** Ensure that the `.env` file is added to `.gitignore` to prevent it from being pushed to version control.

```gitignore
# Environment Variables
.env
```

## Usage

### Running the Bot

Run the Telegram Weather Bot using the following command:

```bash
python weather_bot.py
```

The bot will start polling for messages. Ensure that your environment variables are correctly set in the `.env` file.

## Example

### User Interaction

#### Starting the Bot

```yaml
User: /start
Bot:
Hello! I am a weather bot.
Enter the name of a city to get the weather.
For example: London
```

#### Requesting Weather Information

```yaml
User: New York
Bot:
🌤 Weather in New York:
🔹 Currently: Clear sky
🌡 Temperature: 25 °C
🌡 Feels like: 27 °C
💧 Humidity: 60%
🔻 Pressure: 1012 hPa
```

#### Asking for Help

```yaml
User: /help
Bot:
Bot accepts city names in English or Ukrainian languages.
Simply enter city's name to get a current weather.
```

## Logging

The application maintains a log file named `app.log` that records all interactions and errors, ensuring that logs are manageable and informative.

### Log File Rotation

To prevent `app.log` from growing indefinitely, log rotation is implemented with the following settings:

- **Max Size:** 5 MB per log file.
- **Backup Count:** Maintains up to 5 backup log files (`app.log`, `app.log.1`, ..., `app.log.5`).

### Accessing Logs

You can view the logs by opening the `app.log` file in your project directory:

```bash
cat app.log
```

#### Sample Log Entries:

```yaml
2024-04-27 12:34:56,789 - INFO - Successful API request for city: London in 0.45 seconds
2024-04-27 12:35:10,123 - ERROR - HTTP error for city 'InvalidCity' in 0.30 seconds: 404 Client Error: Not Found for url: ...
2024-04-27 12:36:00,456 - INFO - User 123456789 started the bot.
2024-04-27 12:36:15,789 - INFO - Received weather request for city: Paris from user 123456789
```

## Project Structure

```bash
telegram-weather-bot/
├── weather_bot.py         # Main script that initializes and runs the Telegram bot
├── logger.py               # Handles logging configuration with log rotation and custom logger setup
├── .env                    # Stores environment variables (TG_TOKEN and API_KEY)
├── app.log                 # Log file that records all relevant events and errors
├── requirements.txt        # Lists all Python dependencies required for the project
├── README.md               # Documentation for the project
├── .gitignore              # Specifies files and directories to be ignored by Git
```

## Requirements

Ensure that the following Python packages are installed. They are listed in the `requirements.txt` file.

```text
aiohttp==3.11.11
python-dotenv==1.0.1
python-telegram-bot==21.9
requests==2.32.3
certifi==2024.12.14
```

**Note:** `logging` and `time` are part of Python's standard library and do not need to be included in `requirements.txt`.

## Contributing

Contributions are welcome! If you'd like to enhance the bot, fix bugs, or add new features, feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.