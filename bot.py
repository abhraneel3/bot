import requests
import os
import json
import asyncio
import random
import datetime
from telegram import Bot

async def send_message(bot, channel_id, message):
    try:
        await bot.send_message(chat_id=channel_id, text=message)
        print(f"Message sent to {channel_id}")
    except Exception as e:
        if "Flood control exceeded" in str(e):
            print("Flood control exceeded. Retrying after 30 Sec.")
            await asyncio.sleep(30)  # Wait for 30 Sec.
            await send_message(bot, channel_id, message)  # Retry sending the message
        else:
            print(f"Failed to send message to {channel_id}: {e}")

def is_today(date_string):
    try:
        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_string, "%B %d, %Y")
        
        # Get today's date
        today = datetime.datetime.now()
        
        # Check if the date extracted from the date string is today's date
        return date.date() == today.date()
    except ValueError:
        # If the date string is invalid, return False
        return False

async def fetch_and_send_data():
    try:
        # Fetching JSON data from the GitHub link
        response = requests.get("https://raw.githubusercontent.com/soumyadeb-git/Fetch-Py/main/data/data2.json")
        
        if response.status_code == 200:
            data = json.loads(response.text)
            
            # Reverse the order of the data
            data.reverse()
            
            # Your Telegram Bot token
            bot_token = os.environ.get('TOKEN')
            
            # List of your Telegram Channel IDs and their respective invitation links
            channels = [
                {"id": "@govtjobsector", "invite_link": "https://t.me/govtjobsector"},
                {"id": "@government_job_hunter", "invite_link": "https://t.me/government_job_hunter"}
                # Add more channels if needed
            ]
            
            # Initialize the Telegram bot
            bot = Bot(token=bot_token)
            
            # Emojis and reactions for posts
            emojis = ["💼", "📝", "👩‍💼", "👨‍💼", "💻", "📅", "🏢", "👉", "🔍", "✅", "➡️"]
            
            # Sending messages to each Telegram channel
            for channel in channels:
                channel_id = channel["id"]
                invite_link = channel["invite_link"]
                print(f"Sending messages to {channel_id}")
                for article in data:
                    # Check if all required fields are present
                    if all(key in article for key in ('Title', 'Updated On', 'Last Date', 'Link', 'Summary')):
                        # Check if the update date is today
                        if is_today(article['Updated On']):
                            # Construct and send the message
                            message = (
                                f"{random.choice(emojis)} {article.get('Title', 'N/A')}\n\n"
                                f"➡️ Publish Date: {article.get('Updated On', 'N/A')}\n"
                                f"👉 Location: {article.get('Location', 'Pan India')}\n"
                                f"⚠️ {article.get('Summary', 'N/A')}\n"
                                f" \n\n"
                                f"#job #career #governmentjobs #sarkarinaukri #sarkarijob"
                            )
                            await send_message(bot, channel_id, message)
                            # Introduce a delay between messages
                            await asyncio.sleep(1)  # Adjust the delay time as needed
                    else:
                        print("Skipping article as it is missing required fields")

                # Send custom invitation message
                invitation_message = (
                    f"📢 Don't miss out on daily updates from our Telegram channel!\n\n"
                    f"➡️ Follow the latest government job opportunities and updates.\n\n"
                    f"🔗 Invite your friends who are seeking government jobs to join us too!"
                )
                await send_message(bot, channel_id, invitation_message)
        else:
            print("Failed to fetch data from GitHub")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_and_send_data())
