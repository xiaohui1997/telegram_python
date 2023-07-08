### 内联菜单带回调
#### 预览图片
![image](https://github.com/xiaohui1997/telegram_python/assets/46491804/c163b387-9129-4995-a32c-0f404d3ebf9d)
```
async def menu_button_commands(update: Update, context: CallbackContext) -> None:
    # 创建一个菜单按钮
    button = InlineKeyboardButton(text='菜单按钮', callback_data='menu_button')
    button1 = InlineKeyboardButton(text='菜单按钮1', callback_data='menu_button1')

    # 创建一个包含菜单按钮的键盘
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button,button1]])

    # 向聊天发送带有键盘的消息
    await update.message.reply_text(text='这是一个带有菜单按钮的消息。',
                              reply_markup=keyboard)
  
  # 定义回调查询处理程序
async def handle_menu_button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print(query)
    if query.data == "menu_button":
        # 在聊天中发送一个文本消息，指示菜单按钮被点击了
        await query.edit_message_text(text='你点击了菜单按钮！')
    elif query.data == "menu_button1":
        # 在聊天中发送一个文本消息，指示菜单按钮被点击了
        await query.edit_message_text(text='你点击了菜单按钮1')

# 添加菜单按钮命令处理程序
app.add_handler(CommandHandler('menu', menu_button_commands))

# 添加回调查询处理程序
app.add_handler(CallbackQueryHandler(handle_menu_button_click))
```
### 菜单带回调
#### 预览图片
![image](https://github.com/xiaohui1997/telegram_python/assets/46491804/f9bab22b-6365-4122-99b7-1d217e492742)
```
from telegram import Update, MenuButtonDefault, Bot, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Application, CallbackQueryHandler, \
    ConversationHandler, MessageHandler, filters, CallbackContext
import logging
# 设置日志等级为 INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 回复内容
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'这个群组或频道的 chat_id 是：{chat_id}')
    # 向聊天发送消息，并添加键盘
    await bot.send_message(chat_id=chat_id, text='菜单按钮', reply_markup=keyboard
                           )

# 定义回调查询处理函数
async def handle_menu_button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    print(query)
    if query.data == "menu_button":
        # 在聊天中发送一个文本消息，指示菜单按钮被点击了
        await query.edit_message_text(text='你点击了菜单按钮！')
    elif query.data == "menu_button1":
        # 在聊天中发送一个文本消息，指示菜单按钮被点击了
        await query.edit_message_text(text='你点击了菜单按钮1')


# 添加token
app = ApplicationBuilder().token("6366293079:AAGdHv9CKYaVOU6BAfMpOH1tXssI-hEFgbc").build()

# 创建一个 Bot 对象
bot = Bot(token='6366293079:AAGdHv9CKYaVOU6BAfMpOH1tXssI-hEFgbc')

# 创建键盘按钮
button1 = KeyboardButton(text='fanye')
button2 = KeyboardButton(text='按钮2')
button3 = KeyboardButton(text='按钮3')
button4 = KeyboardButton(text='按钮3')
button5 = KeyboardButton(text='按钮3')
button6 = KeyboardButton(text='按钮3')
button7 = KeyboardButton(text='按钮3')
button8 = KeyboardButton(text='按钮3')
button9 = KeyboardButton(text='按钮3')
button10 = KeyboardButton(text='按钮3')



# 创建键盘并添加按钮
keyboard = ReplyKeyboardMarkup(keyboard=[[button1, button2], [button3],[button4],[button5],[button6],[button7],[button8],[button9],[button10]],
                               resize_keyboard=True,one_time_keyboard=True)


# 定义快捷按钮命令处理程序
async def shortcut_button_commands(update: Update, context: CallbackContext) -> None:
    print(1234)
    text = update.message.text
    print(text)
    if text == '按钮1':
        await update.message.reply_text(text='你点击了按钮1！')

    elif text == '按钮2':
        await update.message.reply_text(text='你点击了按钮2！')

    elif text == '按钮3':
        await update.message.reply_text(text='你点击了按钮3！')

# 添加命令
app.add_handler(CommandHandler("hello", hello))

app.add_handler(CommandHandler("hello", hello))

# app.add_handler(CommandHandler("hello2", handle_menu_button_click))
#app.add_handler(CommandHandler("123", callback=shortcut_button_commands))
app.add_handler(MessageHandler(filters.TEXT, shortcut_button_commands))


# 添加回调查询处理程序
#app.add_handler(CallbackQueryHandler(shortcut_button_commands))

app.run_polling()
```
