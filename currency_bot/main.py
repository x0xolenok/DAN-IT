import telebot
import requests
import json
import os
from datetime import datetime, timedelta
from telebot import types
from config import TOKEN, API_URL

bot = telebot.TeleBot(TOKEN)

REQUESTS_FILE = 'last_requests.json'
CACHE_FILE = 'exchange_rates_cache.json'
CACHE_DURATION = timedelta(minutes=5)

CURRENCIES = {
    'UAH': 980,
    'USD': 840,
    'EUR': 978,
    'GBP': 826,
    'PLN': 985,
    'CAD': 124,
    'CHF': 756
}


def init_requests_file():
    """Initialize the requests file if it doesn't exist"""
    if not os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)


def load_cached_rates():
    """Load cached exchange rates if they exist and are fresh"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time < CACHE_DURATION:
                return cache_data['rates']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return None


def save_rates_cache(rates_data):
    """Save exchange rates to cache with timestamp"""
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'rates': rates_data
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)


def get_exchange_rates():
    """Fetch current exchange rates from cache or API"""
    cached_rates = load_cached_rates()
    if cached_rates:
        return cached_rates
    
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        rates_data = response.json()
        save_rates_cache(rates_data)
        return rates_data
    except requests.exceptions.RequestException:
        return None


def find_rate(rates_data, from_currency_code, to_currency_code):
    """Find exchange rate between two currencies"""
    if not rates_data:
        return None
    
    if from_currency_code == to_currency_code:
        return 1.0
    
    # Convert FROM UAH TO other currency
    if from_currency_code == 980:  # FROM UAH
        for rate in rates_data:
            if rate.get('currencyCodeA') == to_currency_code and rate.get('currencyCodeB') == 980:
                rate_value = rate.get('rateSell', rate.get('rateBuy', 1))
                return 1 / rate_value if rate_value != 0 else 0
    
    # Convert FROM other currency TO UAH
    if to_currency_code == 980:  # TO UAH
        for rate in rates_data:
            if rate.get('currencyCodeA') == from_currency_code and rate.get('currencyCodeB') == 980:
                return rate.get('rateSell', rate.get('rateBuy'))
    
    # Cross rate conversion (non-UAH to non-UAH)
    from_to_uah = None
    to_to_uah = None
    
    for rate in rates_data:
        if rate.get('currencyCodeA') == from_currency_code and rate.get('currencyCodeB') == 980:
            from_to_uah = rate.get('rateSell', rate.get('rateBuy'))
        elif rate.get('currencyCodeA') == to_currency_code and rate.get('currencyCodeB') == 980:
            to_to_uah = rate.get('rateSell', rate.get('rateBuy'))
    
    if from_to_uah and to_to_uah:
        return from_to_uah / to_to_uah
    
    return None


def save_request(amount, from_currency, to_currency, result):
    """Save conversion request to JSON file (keep last 10)"""
    try:
        with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
            requests_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        requests_history = []
    
    new_request = {
        'timestamp': datetime.now().isoformat(),
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'result': result
    }
    
    requests_history.append(new_request)
    
    if len(requests_history) > 10:
        requests_history = requests_history[-10:]
    
    with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(requests_history, f, indent=2, ensure_ascii=False)


def create_currency_keyboard():
    """Create inline keyboard with currency options"""
    keyboard = types.InlineKeyboardMarkup()
    
    row1 = [
        types.InlineKeyboardButton("UAH", callback_data="source_UAH"),
        types.InlineKeyboardButton("USD", callback_data="source_USD"),
        types.InlineKeyboardButton("EUR", callback_data="source_EUR")
    ]
    row2 = [
        types.InlineKeyboardButton("GBP", callback_data="source_GBP"),
        types.InlineKeyboardButton("PLN", callback_data="source_PLN"),
        types.InlineKeyboardButton("CAD", callback_data="source_CAD")
    ]
    row3 = [
        types.InlineKeyboardButton("CHF", callback_data="source_CHF")
    ]
    
    keyboard.row(*row1)
    keyboard.row(*row2)
    keyboard.row(*row3)
    
    return keyboard


def create_target_currency_keyboard(source_currency):
    """Create inline keyboard for target currency selection"""
    keyboard = types.InlineKeyboardMarkup()
    
    available_currencies = [curr for curr in CURRENCIES.keys() if curr != source_currency]
    buttons = []
    
    for currency in available_currencies:
        button = types.InlineKeyboardButton(currency, callback_data=f"target_{currency}")
        buttons.append(button)
    
    for i in range(0, len(buttons), 3):
        keyboard.row(*buttons[i:i+3])
    
    return keyboard


def perform_conversion(user_id, amount, source_currency, target_currency):
    """Perform currency conversion"""
    rates_data = get_exchange_rates()
    
    if not rates_data:
        return None, "❌ Помилка отримання курсу валют. Спробуйте пізніше."
    
    source_code = CURRENCIES.get(source_currency)
    target_code = CURRENCIES.get(target_currency)
    
    if not source_code or not target_code:
        return None, "❌ Невідома валюта."
    
    rate = find_rate(rates_data, source_code, target_code)
    
    if rate is None:
        return None, f"❌ Курс для {source_currency} → {target_currency} не знайдено."
    
    converted_amount = round(amount * rate, 2)
    save_request(amount, source_currency, target_currency, converted_amount)
    
    # Clean up user data
    if hasattr(bot, 'user_data') and user_id in bot.user_data:
        del bot.user_data[user_id]
    
    result_text = f"""✅ **Конвертація виконана!**

💰 **{amount} {source_currency}** → **{converted_amount} {target_currency}**
📈 Курс: 1 {source_currency} = {rate:.4f} {target_currency}

_Курс актуальний на момент запиту від Monobank_

🔄 Для нової конвертації введіть суму"""
    
    return result_text, None

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """Handle start command and show help"""
    if hasattr(bot, 'user_data') and message.from_user.id in bot.user_data:
        del bot.user_data[message.from_user.id]
    
    welcome_text = """🔄 **Ласкаво просимо до валютного конвертера!**

Цей бот допоможе вам конвертувати валюти за поточним курсом від Monobank.

**Як користуватися:**
1. Введіть суму для конвертації (наприклад: 1000)
2. Виберіть валюту, з якої конвертувати
3. Виберіть валюту, в яку конвертувати
4. Отримайте результат конвертації

**Підтримувані валюти:** UAH, USD, EUR, GBP, PLN, CAD, CHF

**Команди:**
/start - Показати це повідомлення
/history - Показати останні 5 конвертацій
/refresh - Оновити курси валют

Введіть суму для конвертації! 💰"""
    
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['refresh'])
def handle_refresh(message):
    """Force refresh exchange rates"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    
    rates_data = get_exchange_rates()
    if rates_data:
        bot.reply_to(message, "✅ Курси валют успішно оновлені!")
    else:
        bot.reply_to(message, "❌ Помилка оновлення курсів валют.")

@bot.message_handler(commands=['history'])
def handle_history(message):
    """Show last 5 conversion requests"""
    try:
        with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
            requests_history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        bot.reply_to(message, "Історія конвертацій порожня.")
        return
    
    if not requests_history:
        bot.reply_to(message, "Історія конвертацій порожня.")
        return
    
    history_text = "📊 **Останні конвертації:**\n\n"
    
    for request in requests_history[-5:]:
        timestamp = datetime.fromisoformat(request['timestamp']).strftime('%d.%m.%Y %H:%M')
        history_text += f"🕐 {timestamp}\n"
        history_text += f"💰 {request['amount']} {request['from_currency']} → {request['result']} {request['to_currency']}\n\n"
    
    bot.reply_to(message, history_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all text messages"""
    if not hasattr(bot, 'user_data'):
        bot.user_data = {}
    
    user_data = bot.user_data.get(message.from_user.id, {})
    
    # Check if user is selecting source currency
    if 'amount' in user_data and 'source_currency' not in user_data:
        currency_input = message.text.upper().strip()
        if currency_input in CURRENCIES:
            bot.user_data[message.from_user.id]['source_currency'] = currency_input
            
            available_currencies = [curr for curr in CURRENCIES.keys() if curr != currency_input]
            currency_list = ", ".join(available_currencies)
            
            keyboard = create_target_currency_keyboard(currency_input)
            
            msg_text = f"""💰 Сума: {user_data['amount']}
1️⃣ З валюти: {currency_input}

2️⃣ Виберіть валюту, В ЯКУ конвертувати:
🔤 **Введіть код:** {currency_list}"""

            bot.reply_to(message, msg_text, reply_markup=keyboard)
            return
        else:
            available_currencies = ", ".join(CURRENCIES.keys())
            bot.reply_to(message, f"❌ Невідома валюта '{currency_input}'\n\n🔤 **Доступні валюти:** {available_currencies}")
            return
    
    # Check if user is selecting target currency  
    elif 'amount' in user_data and 'source_currency' in user_data:
        currency_input = message.text.upper().strip()
        source_currency = user_data['source_currency']
        
        if currency_input in CURRENCIES and currency_input != source_currency:
            result_text, error_text = perform_conversion(
                message.from_user.id, 
                user_data['amount'], 
                source_currency, 
                currency_input
            )
            
            if result_text:
                bot.reply_to(message, result_text, parse_mode='Markdown')
            else:
                bot.reply_to(message, error_text)
            return
        elif currency_input == source_currency:
            bot.reply_to(message, f"❌ Цільова валюта не може бути такою ж як вихідна ({source_currency})")
            return
        else:
            available_currencies = [curr for curr in CURRENCIES.keys() if curr != source_currency]
            currency_list = ", ".join(available_currencies)
            bot.reply_to(message, f"❌ Невідома валюта '{currency_input}'\n\n🔤 **Доступні валюти:** {currency_list}")
            return
    
    # Try to parse as amount
    try:
        amount = float(message.text.replace(',', '.'))
        if amount <= 0:
            bot.reply_to(message, "❌ Сума повинна бути більше нуля. Спробуйте ще раз.")
            return
        
        bot.user_data[message.from_user.id] = {'amount': amount}
        
        keyboard = create_currency_keyboard()
        available_currencies = ", ".join(CURRENCIES.keys())
        
        msg_text = f"""💰 Сума: {amount}

1️⃣ Виберіть валюту, З ЯКОЇ конвертувати:
🔤 **Введіть код:** {available_currencies}"""
        
        bot.reply_to(message, msg_text, reply_markup=keyboard)
        
    except ValueError:
        bot.reply_to(message, "❌ Неправильний формат суми. Введіть число (наприклад: 1000 або 1500.50)")

@bot.callback_query_handler(func=lambda call: call.data.startswith('source_'))
def handle_source_currency_selection(call):
    """Handle source currency selection via button"""
    source_currency = call.data.replace('source_', '')
    user_id = call.from_user.id
    
    if not hasattr(bot, 'user_data'):
        bot.user_data = {}
    
    user_data = bot.user_data.get(user_id, {})
    amount = user_data.get('amount')
    
    if not amount:
        bot.answer_callback_query(call.id, "❌ Сума не знайдена. Введіть суму заново.")
        return
    
    bot.user_data[user_id]['source_currency'] = source_currency
    
    keyboard = create_target_currency_keyboard(source_currency)
    available_currencies = [curr for curr in CURRENCIES.keys() if curr != source_currency]
    currency_list = ", ".join(available_currencies)
    
    try:
        bot.edit_message_text(
            text=f"""💰 Сума: {amount}
1️⃣ З валюти: {source_currency}

2️⃣ Виберіть валюту, В ЯКУ конвертувати:
🔤 **Введіть код:** {currency_list}""",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    except Exception:
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"""💰 Сума: {amount}
1️⃣ З валюти: {source_currency}

2️⃣ Виберіть валюту, В ЯКУ конвертувати:
🔤 **Введіть код:** {currency_list}""",
            reply_markup=keyboard
        )
    
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('target_'))
def handle_target_currency_selection(call):
    """Handle target currency selection via button"""
    target_currency = call.data.replace('target_', '')
    user_id = call.from_user.id
    
    if not hasattr(bot, 'user_data'):
        bot.user_data = {}
    
    user_data = bot.user_data.get(user_id, {})
    amount = user_data.get('amount')
    source_currency = user_data.get('source_currency')
    
    if not amount or not source_currency:
        bot.answer_callback_query(call.id, "❌ Дані не знайдені. Почніть заново.")
        return
    
    bot.answer_callback_query(call.id, "🔄 Виконую конвертацію...")
    
    result_text, error_text = perform_conversion(user_id, amount, source_currency, target_currency)
    
    if result_text:
        bot.edit_message_text(result_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
    else:
        bot.edit_message_text(error_text, call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    init_requests_file()
    get_exchange_rates()
    bot.polling(none_stop=True)
