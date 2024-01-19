# -*- coding: utf-8 -*-

import logging
import re

import telegram
import requests
from flask import Flask, request, jsonify
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Update

# 配置日志信息
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# 创建 Flask 应用
app = Flask(__name__)

# 全局bot变量
bots = None
chat_id = None

#token变量
start_token = '240b093ac0f5de8b7822af95c1bc2beb9a7b912e1f0c1e51976be6698b76e88b'

# 创建 Telegram 机器人处理器
def start(update: Update, context) -> None:
    '''
    :ps 每次重启或者启动需要在群里 /start一下激活变量
    :param update:
    :param context:
    :return:
    '''
    global bots
    global chat_id
    # 获取当前运行环境的公网IP
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            public_ip = data['ip']
            print('当前运行环境的公网IP:', public_ip)
        else:
            print('Error:', response.status_code)
    except requests.RequestException as e:
        print('Error:', str(e))

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text="I'm a bot, please talk to me!\n当前运行环境的公网IP: {}\n api调用当前群chatid:  {}".format(str(public_ip), chat_id))
    bots = context.bot

# 主动发送消息
def sedmsgs(msg, parse_mode=telegram.ParseMode.HTML, chat_id=chat_id):
    '''
    :param msg: 发送的文字
    :param parse_mode: 类型: parse_mode=telegram.ParseMode.MARKDOWN   parse_mode=telegram.ParseMode.HTML
    :return:
    '''
    res = bots.send_message(chat_id, text = msg, parse_mode=parse_mode)
    if res is not None:
        return jsonify({'code': 100003, 'msg': '发送成功'})
    else:
        return jsonify({'code': 100004, 'msg': '发送失败'})

#读取群消息
# 处理群组消息的函数
def handle_group_message(update: Update, context) -> None:
    message = update.message
    chat_id = message.chat_id
    text = message.text

    # 在这里处理群组消息
    # 可以根据需要编写逻辑来响应不同的消息内容
    #企业id 处理--业务
    res = qyid(text)
    if res is not None:
        context.bot.send_message(chat_id=chat_id, text=f"{res[0]}")
        context.bot.send_message(chat_id=chat_id, text=f"{res[1]}")
        context.bot.send_message(chat_id=chat_id, text=f"--"*30)
    # 示例：回复收到的消息
    #context.bot.send_message(chat_id=chat_id, text=f"You said: {text}")

#企业id 处理
def qyid(msg):
    pattern = r"\b(?=\w{25,})(?=.*\d)[a-zA-Z\d]+\b"
    match = re.search(pattern, msg)
    if match:
        valid_string = match.group()
        print("匹配成功，有效字符串为:", valid_string)
        res = requests.post(url='http://127.0.0.1:5000/api/check', data={'qyid': valid_string})
        if res.status_code == 200:
            data = res.json()
            info = '''
            企业id：%s
            
对象存储地址: %s
            ''' % (data['data']['qyid'], data['data']['url'])
            info1 = '''
            所属账号(appid)：%s

所属桶: %s
            ''' % (data['data']['appid'], data['data']['bucketname'])
        return [info, info1]
    else:
        print("未找到匹配的有效字符串")
        return None

@app.route("/")
def index():
    return "hello world"


@app.route("/sendmsg", methods=['POST'])
def sendmsg():
    # 只接受 POST 请求
    if request.method == 'POST':
        token = request.form.get('token')
        msg = request.form.get('msg')
        chatid = request.form.get('chatid')
        if token is None or msg is None or chatid is None:
            info = {
                'code': 100001,
                'msg': '参数不完整'
            }
            return jsonify(info)
        #token校验
        if start_token != token:
            info = {
                'code': 100002,
                'msg': '403'
            }
            return jsonify(info)
        #消息发送
        try:
            res = sedmsgs(msg, chat_id=chatid)
            return res
        except Exception as e:
            print(e)
            return jsonify({'code': 100005, 'info': '请激活bot  run: /start', 'error': str(e)})
    else:
        return 'Method not allowed'

def main():
    # 创建 Updater 对象
    updater = Updater(token='6366293079:AAGdHv9CKYaVOU6BAfMpOH1tXssI-hEFgbc', use_context=True)

    # 获取 Dispatcher 对象
    dispatcher = updater.dispatcher

    # 添加命令处理器
    dispatcher.add_handler(CommandHandler("start", start))

    # 添加 MessageHandler 处理器，指定处理群组消息的函数和过滤器
    group_message_handler = MessageHandler(Filters.group, handle_group_message)
    dispatcher.add_handler(group_message_handler)

    # 启动机器人轮询
    updater.start_polling()

    # 启动 Flask 应用
    app.run(port=8833,host="127.0.0.1")


if __name__ == '__main__':
    main()