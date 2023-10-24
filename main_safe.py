import os
import random
import telebot
import ffmpeg
import requests
import json
import mysql.connector

db_config = {
    "host": "13.56.151.29",
    "user": "thun_tk",
    "password": "Pranavkd44#",
    "database": "thun_tk"
}

TOKEN = '6148411113:AAEb7tXax19l7dQQ5Hx67aJbGf636__c5GU'
bot = telebot.TeleBot(TOKEN)

def upload(file_name):
    try:
        url = 'https://api.nft.storage/upload'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk0NzJjNDY5ZmE4M2M3M0I0YzI2RTQyYThiZjE0NjBkOWFjZWJBNTAiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY5NzgwOTk0ODI2NSwibmFtZSI6Ik5mdCJ9.QNuy4oFt9-fOtksUUe0lcswL4UAuhEZMyXgfFOilTuY',
        }
        files = {'file': open(file_name, 'rb')}
        response = requests.post(url, headers=headers, files=files)
        return response.text
    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, 'Send me a video and reply with !genThumb. I will send you a random thumbnail.')
    except Exception as e:
        print(f"An error occurred while starting the bot: {e}")

@bot.message_handler(func=lambda m: True)
def check_reply(message):
    try:
        if message.reply_to_message and message.text == '!genThumb' and message.reply_to_message.video:
            handle_video(message.reply_to_message)
        elif '!setThumb' in message.text and message.reply_to_message and message.reply_to_message.photo:
            video_post_id = ''.join(filter(str.isdigit, message.text))
            handle_setTumb(message.reply_to_message, video_post_id)
        elif message.reply_to_message and message.text == '!upload' and message.reply_to_message.video:
            handle_video_upload(message.reply_to_message)
    except Exception as e:
        print(f"An error occurred while checking the reply: {e}")

def handle_video_upload(message):
    try:
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
    except Exception as e:
        print(f"An error occurred while handling video upload: {e}")

def handle_video(message):
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        random_number = random.randint(1000000000, 9999999999)
        file_name = str(random_number) + ".mp4"
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Generate thumbnails using ffmpeg
        thumbnails = generate_thumbnails(file_name)

        # Choose 1 random thumbnail
        random_thumbnail = random.choice(thumbnails)

        # Send the thumbnail to the user
        with open(random_thumbnail, 'rb') as f:
            bot.send_photo(message.chat.id, f)
    except Exception as e:
         print(f"An error occurred while handling video: {e}")

def handle_setTumb(message, video_post_id):
    try:
        # Get the largest size photo
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        largest_photo = max(message.photo, key=lambda p: p.width * p.height)
        
        file_info = bot.get_file(largest_photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        random_number = random.randint(1000000000, 9999999999)
        file_name = str(random_number) + ".jpg"
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        res = upload(file_name)
        res_json = json.loads(res)
        cid = res_json['value']['cid']
        
        file_url = f"https://{cid}.ipfs.dweb.link/{file_name}"
        cursor.execute("UPDATE qa_posts SET content = %s WHERE qa_posts.postid = %s", (file_url, video_post_id))
        connection.commit()
        bot.reply_to(message, "Thubnail Set Success" + file_url)
    except Exception as e:
         print(f"An error occurred while setting the thumbnail: {e}")
def generate_thumbnails(video_file):
    thumbnails = []
    stream = ffmpeg.input(video_file)
    random_number = random.randint(1000000000, 9999999999)
    for i in range(5):
        output_file = f'{random_number}{i}.jpg'
        ffmpeg.output(stream, output_file, vframes=1, ss=i).run()
        thumbnails.append(output_file)
    return thumbnails

bot.polling()
