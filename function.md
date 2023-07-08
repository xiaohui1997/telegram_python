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

# 添加回调查询处理程序
app.add_handler(CallbackQueryHandler(handle_menu_button_click))
```
