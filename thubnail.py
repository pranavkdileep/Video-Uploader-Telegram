import os
import random
import telebot
import ffmpeg

TOKEN = '6425191207:AAGO9zzmgF3FYrIKE8-TibgTcPqMr_u9Hck'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Send me a video and reply with !genThumb. I will send you a random thumbnail.')

@bot.message_handler(func=lambda m: True)
def check_reply(message):
    if message.reply_to_message and message.text == '!genThumb' and message.reply_to_message.video:
        handle_video(message.reply_to_message)

def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('video.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # Generate thumbnails using ffmpeg
    thumbnails = generate_thumbnails('video.mp4')

    # Choose 1 random thumbnail
    random_thumbnail = random.choice(thumbnails)

    # Send the thumbnail to the user
    with open(random_thumbnail, 'rb') as f:
        bot.send_photo(message.chat.id, f)

def generate_thumbnails(video_file):
    thumbnails = []
    stream = ffmpeg.input(video_file)
    for i in range(10):
        output_file = f'thumbnail{i}.jpg'
        ffmpeg.output(stream, output_file, vframes=1, ss=i).run()
        thumbnails.append(output_file)
    return thumbnails

bot.polling()
