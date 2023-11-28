from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import change_banner_if_new_post

async def start(update, context):
    await update.message.reply_text('Hello! Send me a command.')

async def echo(update, context):
    received_text = update.message.text
    print(f"Received text: {received_text}")
    if received_text.lower() == "u":
        await update.message.reply_text("Updating banner...")
        change_banner_if_new_post.update_banner_if_new_post()
        await update.message.reply_text("Banner updated successfully!")
    await update.message.reply_text("u - update banner")

def main():
    with open('/home/lunkwill/projects/Lemmy_mod_tools/telegram_lunkstealth_bot_auth.txt', 'r') as f:
        token = f.read()

    bot = Bot(token)  # Create a Bot instance

    # Build the application
    application = ApplicationBuilder().token(token).build()

    # Add handlers to the application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the application
    application.run_polling()

if __name__ == '__main__':
    main()
