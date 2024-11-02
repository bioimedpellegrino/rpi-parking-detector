import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from detector import Detector

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN") 
        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
        self.is_camera_active = False
        self.add_handlers()

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("snap", self.send_snapshot))
        self.dispatcher.add_handler(CommandHandler("send", self.send_attachment))
        self.dispatcher.add_handler(CommandHandler("activate_camera", self.activate_camera))
        self.dispatcher.add_handler(CommandHandler("deactivate_camera", self.deactivate_camera))
        
    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Ciao zio! Per vedere la situazione dei parcheggi. Usa /snap.')

    def send_attachment(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        file_path = os.path.join('..', 'media', 'image.jpg')
        try:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        except FileNotFoundError:
            update.message.reply_text('File non trovato.')
    
    def activate_camera(self, update: Update, context: CallbackContext) -> None:
        try:
            self.detector = Detector()
            self.is_camera_active = True
            update.message.reply_text('Camera operativa')
        except Exception as e:
            print(e)
            update.message.reply_text('Inizializzazione della camera fallita')
            
        
    def deactivate_camera(self, update: Update, context: CallbackContext) -> None:
        try:
            self.detector.close()
            self.is_camera_active = False
            update.message.reply_text('Camera spenta')
        except Exception as e:
            print(e)
            update.message.reply_text('Spegnimento della camera fallito. Riavviare...')
        
            
    def send_snapshot(self, update: Update, context: CallbackContext) -> None:
        
        if not self.is_camera_active:
            update.message.reply_text('La camera non è inizializzata. Per inizializzara invia: /activate_camera')
            return
            
        chat_id = update.effective_chat.id
        
        attach_path = self.detector.take_snapshot()
        attach_path = attach_path if attach_path else "image.jpg"
        file_path = os.path.join('..', 'media', attach_path)
        update.message.reply_text("Ecco a te zio")
        try:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        except FileNotFoundError:
            update.message.reply_text('File non trovato.')

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
