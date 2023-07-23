import telebot
import requests

# 设置Telegram Bot的API密钥
telegram_token = '6319005725:AAE1-rPuBENSD-Mff1o2M0egBRgASeOr_vs'
bot = telebot.TeleBot(telegram_token)

# 保存用户的OpenAI API密钥
users_api_keys = {}  # 用字典来保存不同用户的API密钥

# 定义命令处理程序
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users_api_keys:
        bot.reply_to(message, '欢迎使用OpenAI余额查询机器人！在开始查询余额之前，请先输入您的OpenAI API密钥，发送 /set_api_key <YOUR_API_KEY> 来设置密钥。')
    else:
        bot.reply_to(message, '您已经设置了API密钥，请发送 /balance 来查询帐户余额。')

@bot.message_handler(commands=['set_api_key'])
def set_api_key(message):
    user_id = message.from_user.id
    api_key = message.text.split(' ')[1]

    # 保存用户的API密钥
    users_api_keys[user_id] = api_key
    bot.reply_to(message, '已保存您的API密钥，请发送 /balance 来查询帐户余额。')

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    if user_id not in users_api_keys:
        bot.reply_to(message, '您还未设置API密钥，请先发送 /set_api_key <YOUR_API_KEY> 来设置密钥。')
    else:
        try:
            # 使用用户提供的API密钥调用OpenAI API获取帐户余额
            api_key = users_api_keys[user_id]
            session_key = api_key
            url = "https://api.openai.com/dashboard/billing/credit_grants"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {session_key}"
            }

            response = requests.get(url, headers=headers)
            data = response.json()

            # 提取可用余额
            total_available_balance = data.get('total_available', 0.0)

            bot.reply_to(message, f'您的OpenAI帐户余额为：{total_available_balance} 美元。')
        except Exception as e:
            bot.reply_to(message, f'查询失败：{str(e)}')

# 启动机器人
bot.polling()
