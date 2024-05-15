import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from chat import chat

TOKEN = os.environ.get('TELEGRAM_TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME')

# Command


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Hello! Thanks for chatting with me! I a UMGB Bot')


# end def


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()

        else:
            return
    else:
        response = chat(text)

        helper = response.find('{')

        if helper > 0:

            # To split and see what help is needed
            helper_selector = response[helper:]

            # spliting the help request from the main response
            response = response[:helper] + f"\nSending resources...."

            # sending a response first before the help request
            await update.message.reply_text(response)

            if helper_selector.find('PDF') > 0:

                await context.bot.sendDocument(update.effective_chat.id, document=open(
                    helper_selector[6:], "rb"))

            elif helper_selector.find('MAP') > 0:

                map_location = helper_selector[6:]
                map_location = map_location.split(",")
                map_data = []

                for i, data in enumerate(map_location):
                    map_data.append(data)

                    if ((i+1) % 3 == 0):

                        await update.message.reply_text(map_data[0])
                        await context.bot.sendLocation(update.effective_chat.id, latitude=map_data[1], longitude=map_data[2])

                        map_data = []
        else:
            await update.message.reply_text(response)

# end def


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} cause error {context.error}")

if __name__ == "__main__":
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("Polling....")
    app.run_polling(poll_interval=3)
# end main
