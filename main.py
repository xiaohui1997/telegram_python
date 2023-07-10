# -*- coding: utf-8 -*-

import logging
import telegram
from flask import Flask, request, jsonify
from telegram.ext import Updater, CommandHandler
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
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text="I'm a bot, please talk to me!")
    bots = context.bot

# 主动发送消息
def sedmsgs(msg, parse_mode=telegram.ParseMode.HTML):
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


@app.route("/")
def index():
    return "hello world"


@app.route("/sendmsg", methods=['POST'])
def sendmsg():
    # 只接受 POST 请求
    if request.method == 'POST':
        token = request.form.get('token')
        msg = request.form.get('msg')
        if token is None or msg is None:
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
            res = sedmsgs(msg)
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

    # 启动机器人轮询
    updater.start_polling()

    # 启动 Flask 应用
    app.run(port=8833,host="127.0.0.1")


if __name__ == '__main__':
    main()