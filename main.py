from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, MessageFilter, CallbackContext
import config  # فایل کانفیگ

# ایجاد یک نمونه از bot با token داده شده
bot = Bot(token=TOKEN)

# تابع پاسخ به message  دریافت شده، پیام ارسال شده به ادمین
def message(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id == int(ADMIN_ID):
        return
    text = f"Message from {user.first_name} (ID: {user.id}):\n{text}"
    bot.send_message(chat_id=ADMIN_ID, text=text)

# تابع پاسخ به دستور /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام، به ربات خودتون خوش آمدید!')

# تابع پاسخ به دستور /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('لیست دستورها:')

# تابع پاسخ به دستور /echo
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# تابع پاسخ به دستور /admin
def admin_message(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == int(ADMIN_ID):
        bot.send_message(chat_id=context.args[0], text=context.args[1])

# تابع main برای ایجاد Updater و Dispatcher و اضافه کردن دستورات
def main():
    # ایجاد یک نمونه از Updater با token داده شده
    updater = Updater(TOKEN)

    # ایجاد یک dispatcher
    dispatcher = updater.dispatcher

    # تعریف دستورات
    message_handler = MessageHandler(Filters.text & (~Filters.command), message)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    echo_handler = CommandHandler('echo', echo)
    admin_handler = CommandHandler('admin', admin_message, pass_args=True)

    # افزودن دستورات به dispatcher
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(admin_handler)

    # شروع پایینگ
    updater.start_polling()

    # رفتار در شرایط نامطلوب اینجا تعیین شده است
    updater.idle()

# شروع اجرا
if __name__ == '__main__':
    main()
