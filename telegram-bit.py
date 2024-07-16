from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Send me an image!')

def image_handler(update, context):
    file_id = update.message.photo[-1].file_id
    file_info = context.bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_url)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Starting Bot....")
    app = Application.builder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
  

    # MESSAGES
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # ERROR
    app.add_error_handler(error)

    # check for updates
    # poll the bot
    print("Polling...")
    app.run_polling(poll_interval=1)  # for 5 seconds