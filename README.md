# Telegram Channel Helper Bot

## Overview

Telegram Channel Helper is a sophisticated Telegram bot designed to facilitate
channel management, user interactions, and administrative tasks. The bot
provides a robust set of features for managing communication between users and
channel administrators.

## Key Features

- User message forwarding to admin chat
- Media group handling
- User ban/unban management
- Dynamic message creation for channels
- Configurable bot settings

## Prerequisites

- Python 3.10+
- Redis (as project database)
- Telegram Bot API Token (see [botfather](https://t.me/botfather))

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/smkthat/tg-channel-helper.git | cd tg-channel-helper
```

### 2. Create Virtual Environment

```bash
make setup
```

This command will:

- Create a Python virtual environment
- Install all required dependencies from `requirements.txt`

### 3. Configuration

1. Create a `.env` file in the project root (see `.env.template` for example)
2. Add the following environment variables

```env
BOT_1234567890=your_telegram_bot_token
# Where "1234567890" is the bot ID
# Add more bot tokens if needed
```

3. Modify `default.yaml` to configure bot settings (see `default.example.yaml`):

- Set debug mode
- Configure bot IDs
- Define admin chat settings

### 4. Database Setup

Ensure Redis is installed and running on your system.

### 5. Run the Bot

```bash
make run
```

### 6. Development Commands

- `make test`: Run test suite
- `make lint`: Run code quality checks
- `make clean`: Remove virtual environment and cache

## Project Structure

```
tg-channel-helper/
│
├── app/
│   ├── configuration/     # Configuration management
│   ├── handlers/          # Message and callback handlers
│   ├── db/                # Database interactions
│   ├── services/          # Business logic services
│   └── middlewares/       # Request processing middlewares
│
├── tests/                 # Unit and integration tests
├── logs/                  # Application logs
├── Makefile               # Build and development commands
└── requirements.txt       # Python dependencies
```

## Environment Variables

- `BOT_{ID}`: (Required) Telegram Bot API tokens
- `REDIS_PASSWORD`: (Optional) Redis password
- Additional environment variables can be configured in `.env` file

## Logging

Logs are stored in the `logs/` directory with detailed application events and
error tracking.

## Contribution

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.