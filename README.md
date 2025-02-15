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

### 4. Bot Configuration (`bot_data.yaml`)

#### Overview

The `bot_data.yaml` file is a crucial configuration file that allows you to customize bot behavior for each Telegram bot instance. This file uses the bot's numeric ID as the key and supports various configuration options.

#### Configuration Structure

```yaml
<bot_id>:
  start_message:
    text: 'Customizable start message with {user_mention} placeholder'
    buttons:
      - - text: 'Button Text'
          url: 'Button URL'
    after:
      - text: 'Additional message'
        ttl: 3 # Message display time in seconds
  answer_message:
    text: 'Response message'
    ttl: 3 # Response message display time in seconds
```

#### Key Components

- `<bot_id>`: Unique Telegram bot identifier
- `start_message`:
  - `text`: Greeting message with optional `{user_mention}` placeholder
  - `buttons`: Nested array of buttons with text and URL
  - `after`: Additional messages with time-to-live (TTL)
- `answer_message`:
  - `text`: Automated response message
  - `ttl`: Time in seconds the message will be displayed

#### Example Configuration

```yaml
12345678:
  start_message:
    text: '👋🏽 Hello, {user_mention}!'
    buttons:
      - - text: '📄 Docs'
          url: 'https://github.com/smkthat/tg-channel-helper'
      - - text: '👨🏽‍💻 Author'
          url: 'https://t.me/smkthat'
    after:
      - text: '📩 All messages you send will be forwarded to the channel team 🤗'
        ttl: 3
  answer_message:
    text: '✅ Thank you, we received your message!'
    ttl: 3
```

#### Getting Started

1. Copy `bot_data.example.yaml` to `bot_data.yaml`
2. Replace `<bot_id>` with your actual Telegram bot's numeric ID
3. Customize messages, buttons, and behavior as needed

**Note**: Ensure you keep sensitive information confidential and do not commit `bot_data.yaml` to version control.

### 5. Database Setup

Ensure Redis is installed and running on your system.

### 6. Run the Bot

```bash
make run
```

### 7. Development Commands

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
│
├── Makefile               # Build and development commands
├── .env.example           # Example environment variables
├── bot_data.example.yaml  # Example bot configuration
├── default.yaml           # Default configuration
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