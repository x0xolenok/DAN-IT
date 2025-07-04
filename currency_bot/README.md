# Currency Converter Telegram Bot

A Telegram bot for converting between different currencies using real-time exchange rates from Monobank API.

## Features

- **Any-to-any currency conversion** between supported currencies (UAH, USD, EUR, GBP, PLN, CAD, CHF)
- **Smart caching system** - caches exchange rates for 5 minutes to reduce API calls
- **Two-step selection process** - choose source currency, then target currency
- **Cross-rate calculations** - supports direct conversion between non-UAH currencies
- **Interactive UI** with inline keyboards for easy currency selection
- **Conversion history** - saves last 10 conversions to JSON file
- **Real-time rates** from Monobank API with automatic cache management

## Supported Currencies

🇺🇦 **UAH** (Ukrainian Hryvnia)  
🇺🇸 **USD** (US Dollar)  
🇪🇺 **EUR** (Euro)  
🇬🇧 **GBP** (British Pound)  
🇵🇱 **PLN** (Polish Zloty)  
🇨🇦 **CAD** (Canadian Dollar)  
🇨🇭 **CHF** (Swiss Franc)  

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Telegram Bot Token:**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Copy the token

3. **Configure the bot:**
   - Open `config.py`
   - Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` with your actual bot token

4. **Run the bot:**
   ```bash
   python main.py
   ```

## Usage

1. Start a conversation with your bot
2. Send `/start` to see welcome message
3. **Enter amount** to convert (e.g., `1000`)
4. **Select source currency** (what you're converting from)
5. **Select target currency** (what you're converting to)
6. Get the conversion result instantly!

## Commands

- `/start` or `/help` - Show welcome message and instructions
- `/history` - Show last 5 conversions
- `/refresh` - Force refresh exchange rates (clears cache)

## Example Conversions

- **1000 UAH → USD** (Ukrainian Hryvnia to US Dollar)
- **500 EUR → GBP** (Euro to British Pound)  
- **100 USD → PLN** (US Dollar to Polish Zloty)
- **And any other combination!**

## Technical Features

### Smart Caching System
- **5-minute cache duration** for exchange rates
- **Automatic cache management** - no manual intervention needed
- **Reduced API calls** - only fetches fresh data when cache expires
- **Faster responses** - most conversions use cached data

### Cross-Rate Calculations
- **Direct conversions** when possible (e.g., USD → UAH)
- **Cross-rate calculations** for indirect pairs (e.g., USD → EUR via UAH)
- **Accurate rates** using Monobank's official exchange rates

## Files

- `main.py` - Main bot logic with caching and conversion features
- `config.py` - Configuration (bot token, API URL)
- `requirements.txt` - Python dependencies  
- `last_requests.json` - Auto-created conversion history storage
- `exchange_rates_cache.json` - Auto-created exchange rates cache 