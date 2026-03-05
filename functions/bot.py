import json
import os
import asyncio
from telegram import Bot, Update
from telegram.constants import ParseMode

# 1. Get the token from environment variables
TOKEN = os.environ.get("BOT_TOKEN")

async def main(event, context):
    # 2. Initialize the bot
    bot = Bot(token=TOKEN)

    try:
        # 3. Parse the incoming update from Telegram
        body = json.loads(event["body"])
        update = Update.de_json(body, bot)

        # 4. Check if the update is a text message
        if update.message and update.message.text:
            chat_id = update.message.chat_id
            message_id = update.message.message_id
            original_text = update.message.text

            # 5. Send the new Monospace message
            # We use triple backticks ``` for monospace block
            formatted_text = f"```\n{original_text}\n```"
            
            await bot.send_message(
                chat_id=chat_id, 
                text=formatted_text, 
                parse_mode=ParseMode.MARKDOWN_V2
            )

            # 6. Delete the user's original message
            # Note: Bot needs ADMIN rights in groups to do this
            try:
                await bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                print(f"Could not delete message: {e}")

        return {"statusCode": 200, "body": "OK"}

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": "Error"}

# Netlify handler wrapper
def handler(event, context):
    return asyncio.run(main(event, context))
          
