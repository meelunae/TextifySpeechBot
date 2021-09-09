import logging
import os
import speech_recognition as sr
import subprocess
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

OGG_PATH = './voice.ogg'
WAV_PATH = './voice.wav'
updater = Updater(token='')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
speech_recognizer = sr.Recognizer()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, welcome to this bot!")

def voiceMessage(update, context):
    file = context.bot.getFile(update.message.voice.file_id)
    file.download(OGG_PATH)
    logger.info("Downloaded voice message successfully.")
    process = subprocess.run(['ffmpeg', '-y', '-i', OGG_PATH, WAV_PATH])
    if process.returncode != 0:
        raise Exception("Something went wrong")
    target = sr.AudioFile(WAV_PATH)
    with target as source:
        speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = speech_recognizer.record(source)
        output = speech_recognizer.recognize_google(audio, language="it-IT")
        context.bot.send_message(chat_id = update.effective_chat.id, text = output)
        os.remove(OGG_PATH)
        os.remove(WAV_PATH)

def main():
    start_handler = CommandHandler('start', start)
    voice_handler = MessageHandler(Filters.voice, voiceMessage)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(voice_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()


