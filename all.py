# Import the required modules
import telebot # To interact with the Telegram API
import os # To work with files and directories
import random # To generate random numbers
import requests
import json

# Create a bot object with the bot token
bot = telebot.TeleBot("6781220318:AAENfg4idKOfWvnGHFor8_Des1kZIkAuPMs")

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
@bot.message_handler(content_types=['document', 'audio', 'photo', 'video'])
def handle_file(message):
    # Get the file id
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name
    elif message.photo:
        file_id = message.photo[-1].file_id  # get the highest resolution photo
        file_name = "photo.jpg"
    elif message.video:
        file_id = message.video.file_id
        file_name = "video.mp4"

    # Get the file information from the bot
    file_info = bot.get_file(file_id)
    # Get the file path from the file information
    file_path = file_info.file_path
    # Download the file from the Telegram server
    downloaded_file = bot.download_file(file_path)
    # Generate a unique random 10-digit number
    random_number = random.randint(1000000000, 9999999999)
    # Create a new file name with the random number and original extension
    new_file_name = str(random_number) + "." + file_name.split('.')[-1]
    # Save the file in the same location as this script
    with open(new_file_name, "wb") as f:
        f.write(downloaded_file)
    # Send a confirmation message to the user
    bot.reply_to(message, "File saved as " + new_file_name) 
    bot.reply_to(message, "Uploading to IPFS...")
    res = upload(new_file_name)
    res_json = json.loads(res)
    cid = res_json['value']['cid']
    file_url = f"https://{cid}.ipfs.w3s.link/{new_file_name}"
    bot.reply_to(message, "Your file Link is " + file_url)
    # Delete the file from the local storage
    os.remove(new_file_name)

# Start polling for updates from the Telegram server
bot.polling()
