from typing import Final
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from io import BytesIO
from ultralytics import YOLO
import cv2
import supervision as sv


TOKEN: Final = "706945219:AAGhFEXYeQEdrJPXUaSPrOaDpLPVu7DeMY4"
BOT_USERNAME: Final = "@OgwalBot"

# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, thanks for chatting with me.")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, this bot is about Open Vision which will assist you in detecting Kenyan coins.")

def handle_responses(text: str) -> str:
    processed: str = text.lower()
    if "hello" in processed:
        return "Hi there"
    return "I don't understand that command."


async def handle_photo(update: Update, context: CallbackContext):
    message_type: str = update.message.chat.type
    photo_file = await update.message.photo[-1].get_file()  # Get the highest resolution photo

    print(f"User: ({update.message.chat.id}) in {message_type} sent a photo.")
    print(photo_file.file_path)
    
    model = YOLO("best.pt")  # load a custom model
    
    # Single stream with batch-size 1 inference
    # source = photo_file.download_as_bytearray() # RTSP, RTMP, TCP or IP streaming address
    
    bio = BytesIO()
    await photo_file.download_to_memory(out=bio)

    # Run inference on the source
    results = model(bio, stream=False)  # generator of Results objects
    
    # Run batched inference on a list of images
    
    # Process results list
    print(results)
    
    bio.close()
    
    detections = sv.Detections.from_ultralytics(results)
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    labels = [
        f"{class_name} {confidence:.2f}"
        for class_name, confidence
        in zip(detections['class_name'], detections.confidence)
    ]

    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)

    # return sv.plot_image(annotated_image, (12, 12))

    await context.bot.send_photo(chat_id=update.message.chat.id, photo= 'second2 image.png', caption= "caption" )#fileName)



    # response: str = f"Photo received and will be sent back."
    # if message_type == "group" and BOT_USERNAME not in (update.message.caption or ""):
    #     return  # Do nothing if bot is not mentioned in the caption in a group chat

    # # Download the photo to memory and send it back to the user
    # bio = BytesIO()
    # await photo_file.download_to_memory(out=bio)
    
    # await update.message.reply_photo(photo=bio, caption="Here is the photo you sent")

    # bio.close()



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User: ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == "group" and BOT_USERNAME not in text:
        return

    new_text: str = text.replace(BOT_USERNAME, "").strip()
    response: str = handle_responses(new_text)
    
    print("Bot:", response)
    await update.message.reply_text(response)
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused the following error: {context.error}")

if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # ERROR
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=1)
  