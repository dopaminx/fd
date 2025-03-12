import asyncio
import random
import logging
from telethon import TelegramClient, events

API_ID = 27062087
API_HASH = "00ec51974dcaeb694b7256b85bf1472c"
SESSION_NAME = "mysession"
GROUP_IDS = [-1002294330311, -1002377547868]
KEYWORDS = ["Charge Successfully", "Charged"]
FORWARD_TO_USER = "t.me/+EQS11Y0NMrJiNzll"
RANDOM_DELAY = (0.5, 2.5)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger("TelegramBot")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

forwarded_messages = set()


@client.on(events.NewMessage(chats=GROUP_IDS))
async def handler(event):
    try:
        delay = random.uniform(*RANDOM_DELAY)
        await asyncio.sleep(delay)

        message_text = event.message.message

        if any(keyword.lower() in message_text.lower()
               for keyword in KEYWORDS):
            if message_text not in forwarded_messages:
                await client.send_message(FORWARD_TO_USER, event.message)
                logger.info("✅ Message forwarded successfully")

                forwarded_messages.add(message_text)
            else:
                logger.info("🚫 Duplicate message ignored")

    except Exception as e:
        logger.error("❌ Error occurred")


async def main():
    logger.info("🤖 Bot is running...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user.")
    except Exception as e:
        logger.error("❌ Error occurred while running the bot")
