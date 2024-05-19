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

def is_yesterday(date_string):
    try:
        # Convert the date string to a datetime object
        date = datetime.datetime.strptime(date_string, "%B %d, %Y")
        
        # Calculate yesterday's date
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        
        # Check if the date extracted from the date string is yesterday's date
        return date.date() == yesterday.date()
    except ValueError:
        # If the date string is invalid, return False
        return False


async def fetch_and_send_data():
    try:
        # Fetching JSON data from the GitHub link
        response = requests.get("https://raw.githubusercontent.com/soumyadeb-git/Fetch-Py/main/data/merged_data.json")
        
        if response.status_code == 200:
            data = json.loads(response.text)
            
            # Reverse the order of the data
            data.reverse()
            
            # Your Telegram Bot token
            bot_token = os.environ.get('TOKEN')
            
            # List of your Telegram Channel IDs and their respective invitation links
            channels = [
                {"id": "@govtjobsector", "invite_link": "https://t.me/+CjTSDbz1tCdhYjY1"},
                {"id": "@government_job_hunter", "invite_link": "https://t.me/+_72f-aO66N8xNTc1"}
                # Add more channels if needed
            ]
            
            # Initialize the Telegram bot
            bot = Bot(token=bot_token)
            
            # Emojis and reactions for posts
            emojis = ["💼", "📝", "👩‍💼", "👨‍💼", "💻", "📅", "🏢", "👉", "🔍", "✅", "➡️"]
            reactions = [
                "Great opportunity!", 
                "Thanks for sharing!", 
                "Good luck to all applicants!", 
                "Keep up the good work!", 
                "Appreciate the update!",
                "Exciting news for job seekers!",
                "Impressive job listing!",
                "Valuable resource for job hunters!",
                "Excellent addition to the channel!",
                "Fantastic opportunity for career growth!",
                "Well done on the job notification!",
                "This will benefit many job seekers!",
                "Superb update for the community!",
                "A must-see for professionals!",
                "Incredible job opening!",
                "Top-notch job listing!",
                "A gem for those seeking employment!"
            ]
            
            # Sending messages to each Telegram channel
            for channel in channels:
                channel_id = channel["id"]
                invite_link = channel["invite_link"]
                print(f"Sending messages to {channel_id}")
                for article in data:
                    # Check if all required fields are present
                    if all(key in article for key in ('Title', 'Updated On', 'Last Date', 'Link')):
                        # Check if the last date is not yesterday
                        if not is_yesterday(article['Last Date']):
                            # Construct and send the message
                            message = (
                                f"{random.choice(emojis)} {article.get('Title', 'N/A')}\n\n"
                                f"➡️ Publish Date: {article.get('Updated On', 'N/A')}\n"
                                f"⏱️ Last Date: {article.get('Last Date', 'N/A')}\n"
                                f"🔗 Apply Link: {article.get('Link', 'N/A')}\n\n"
                                f"{random.choice(reactions)}"
                            )
                            await send_message(bot, channel_id, message)
                            # Introduce a delay between messages
                            await asyncio.sleep(1)  # Adjust the delay time as needed
                    else:
                        print("Skipping article as it is missing required fields")

                # Send custom invitation message
                invitation_message = (
                    f"We Know You Find this Telegram Channel is Helpful. Join our channel for more Daily updates:\n\n"
                    f"Click the link below to Follow Our Channel and We Recommend to You Please Share this Invitation Link with Your Friends, Who are Looking for Government Jobs:\n\n"
                    f"👉 Click Here to Follow Us: {invite_link}"
                )
                await send_message(bot, channel_id, invitation_message)
        else:
            print("Failed to fetch data from GitHub")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_and_send_data())
