import telebot
import requests

TOKEN = "6628625132:AAEw8TwzPMaO07OYkcN-LCbiMihzrO7uTKE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "欢迎使用IP测试机器人！请输入要测试的IP地址。")

@bot.message_handler(func=lambda message: True)
def handle_ip(message):
    user_input = message.text

    # 发送第一个请求
    first_url = "https://zh.rakko.tools/tools/13/pingCheckController.php"
    data = {
        "token_id": "64e829f8b690a",
        "token": "ab64e829f8b6910",
        "hostOrIp": user_input
    }
    
    headers = {
        "Host": "zh.rakko.tools",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
        "Origin": "https://zh.rakko.tools",
        "Referer": "https://zh.rakko.tools/tools/13/",
        "Cookie": "PHPSESSID=ende5ge7g02reod3tqvss8b3he; history_list=%5B%2213%22%5D"
    }
    
    response1 = requests.post(first_url, data=data, headers=headers)
    
    try:
        response_data = response1.json()
        result = response_data.get("result")
        if result is not None:
            # 发送第二个请求获取更多信息
            second_url = f"http://ip-api.com/json/{user_input}"
            response2 = requests.get(second_url)
            response_data2 = response2.json()
            country = response_data2.get("country")
            org = response_data2.get("org")
            
            response_text = f"测试结果: {result}\nIP信息:\n国家: {country}\n组织: {org}"
            bot.reply_to(message, response_text)
        else:
            bot.reply_to(message, "无法获取测试结果。")
    except Exception as e:
        bot.reply_to(message, f"出现错误: {e}")

bot.polling()
