# Import the required modules
import telebot # To interact with the Telegram API
import os # To work with files and directories
import random # To generate random numbers
import requests
import json

# Create a bot object with the bot token
bot = telebot.TeleBot("6148411113:AAEb7tXax19l7dQQ5Hx67aJbGf636__c5GU")

def upload(file_name):
    url = 'https://api.nft.storage/upload'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk0NzJjNDY5ZmE4M2M3M0I0YzI2RTQyYThiZjE0NjBkOWFjZWJBNTAiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5NzgwOTk0ODI2NSwibmFtZSI6Ik5mdCJ9.QNuy4oFt9-fOtksUUe0lcswL4UAuhEZMyXgfFOilTuY',
    }
    files = {'file': open(file_name, 'rb')}
    response = requests.post(url, headers=headers, files=files)

    return response.text




# Define a handler for video messages
@bot.message_handler(content_types=['video'])
def handle_video(message):
    # Get the file id of the video
    file_id = message.video.file_id
    # Get the file information from the bot
    file_info = bot.get_file(file_id)
    # Get the file path from the file information
    file_path = file_info.file_path
    # Download the file from the Telegram server
    downloaded_file = bot.download_file(file_path)
    # Generate a unique random 10-digit number
    random_number = random.randint(1000000000, 9999999999)
    # Create a file name with the random number and .mp4 extension
    file_name = str(random_number) + ".mp4"
    # Save the file in the same location as this script
    with open(file_name, "wb") as f:
        f.write(downloaded_file)
    # Send a confirmation message to the user
    res = upload(file_name)
    res_json = json.loads(res)
    cid = res_json['value']['cid']
    file_url = f"https://{cid}.ipfs.dweb.link/{file_name}"
    bot.reply_to(message, "Your video Link is " + file_url)

# Start polling for updates from the Telegram server
bot.polling()
