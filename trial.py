from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext




import os
from dotenv import load_dotenv
from build_models import process_image, fig2img, count_coins

#Load keys 
load_dotenv()
TELE_BOT_API_KEY= os.getenv('TELE_BOT_API_KEY')
Bot_username= os.getenv('Bot_username')
TOKEN: Final = TELE_BOT_API_KEY
Bot_username: Final = Bot_username


# COMMANDS
# /start command 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, thanks for chatting with me. \n\n"
        "Welcome to OpenVisionBot! This bot is a small project built on the YOLOv8 model with Ultralytics for detecting Kenyan shillings coins. \n\n"
        "To learn how to use the bot, use the /help command. \n\n"
        "For more information, visit the [Ultralytics website](https://ultralytics.com) and check out the [GitHub repository](https://github.com/stevalberts/openvision/tree/master)."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here are the available commands and their descriptions:\n\n"
        "/help - How to run the bot\n"
        "/start - How to start the bot\n"
        "/about - More information about the bot\n"
        "/predict - For detecting the coins and counting the value"
    )

# /Predict command
async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo='openv.jpg')

# /About 
async def about_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello this bot is about open vission which will assist you in detecting kenyan coins")



def handle_responses(text:str) ->str:
    processed:str = text.lower()

    if "hello" in processed:
        return "Hi there"



async def download_image(update:Update, context:CallbackContext):
    # Download file
    fileName = update.message.photo[-1].file_id
    new_file = await update.message.photo[-1].get_file()

    #kk= await new_file.download_to_drive(f"{fileName}.jpg")
    file = await new_file.download_to_drive(f"{fileName}.jpg")

    return file
    
    
async def predict_image(update:Update, context: CallbackContext):
    file= await download_image(update, context)

    if not file:
        await update.message.reply_text("Something went wrong, try again!")
        return
    else:
        await update.message.reply_text("The Image has been uploaded successfully Plesae wait as we process!")
    
    #Process the image through roboflow API
    resp=  process_image(f"{file}")

    #check we have results from the api
    if not resp or len(resp)<= 1:
        await update.message.reply_text("Roboflow: Something went wrong, try again!")
        return
    else:
        img = fig2img(resp[0])
        img.save('second2 image.png') #Save the image
        #count the coins
        coins= count_coins(resp[1])

    # Acknowledge file received
    if not img:
        await update.message.reply_text("The image was not processed, try again!")
        return
    else:
        await update.message.reply_text(f"Compiling.... Please Wait!")
        os.remove(f"{file}")

    # Send the file
    chat_id = update.message.chat.id
    caption=f"Your Image has {coins['Number of coin']} coins amounting to Ksh. {coins['Total amount ']}"

    await context.bot.send_photo(chat_id=chat_id, photo= 'second2 image.png', caption= caption )#fileName)



async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str= update.message.text

    print(f"User: ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type== "group":
        if Bot_username in text:
            new_text:str= text.replace(Bot_username,"").strip()
            response: str=handle_responses(new_text)
        else:
            return
        
    else:
        response:str= handle_responses(text)
    
    print("Bot:", response)
    await update.message.reply_text(response)





async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update: {update} caused the following error, {context.error}")
    #added to call the help function incase we have an error
    await help_command(update, context)


    


if __name__ == "__main__":
    print("Starting Bot....")
    app = Application.builder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler('Predict', predict_command))


    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    #app.add_handler(MessageHandler(filters.PHOTO,handle_image))
    app.add_handler(MessageHandler(filters.ALL, predict_image))
  

    # MESSAGES
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # ERROR
    app.add_error_handler(error)


  

    # check for updates
    # poll the bot
    print("Polling...")
    app.run_polling(poll_interval=1)  # for 5 seconds