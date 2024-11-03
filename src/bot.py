import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from raspi_camera import RaspiCamera
from detector import Detector

load_dotenv()

class TelegramBot:
    def __init__(self, camera: RaspiCamera, detector: Detector, base_dir: str):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN") 
        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
        self.is_camera_active = False
        self.camera = camera
        self.detector = detector
        self.base_dir = base_dir
        self.add_handlers()

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("snap", self.send_snapshot))
        self.dispatcher.add_handler(CommandHandler("send", self.send_attachment))
        self.dispatcher.add_handler(CommandHandler("check", self.check_free_spot))
        self.dispatcher.add_handler(CommandHandler("activate_camera", self.activate_camera))
        self.dispatcher.add_handler(CommandHandler("deactivate_camera", self.deactivate_camera))
        self.dispatcher.add_handler(CommandHandler("register", self.register))
        
    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Ciao zio! Per vedere la situazione dei parcheggi usa /snap. Per essere avvisato quando si libera un parcheggio usa /register')

    def register(self, update: Update, context: CallbackContext) -> None:
        chat_id = str(update.message.chat_id)
        chat_id_file_name = "chat_ids.txt"
        
        if not os.path.exists(os.path.join(self.base_dir, "config")):
            os.makedirs(os.path.join(self.base_dir, "config"))
        
        chat_id_file_path = os.path.join(self.base_dir, "config", chat_id_file_name)
        
        if os.path.exists(chat_id_file_path):
            with open(chat_id_file_path, "r") as file:
                chat_ids = file.read().splitlines()
        else:
            chat_ids = []

        if chat_id not in chat_ids:
            chat_ids.append(chat_id)
            with open(chat_id_file_path, "a") as file:
                file.write(chat_id + "\n")
            update.message.reply_text("Registrazione avvenuta con successo!")
        else:
            update.message.reply_text("Sei già registrato!")
    
    def send_attachment(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        file_path = os.path.join(self.base_dir, 'media', 'image.jpg')
        try:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        except FileNotFoundError:
            update.message.reply_text('File non trovato.')
    
    def check_free_spot(self, update: Update, context: CallbackContext) -> None:
        
        if not self.is_camera_active:
            update.message.reply_text('La camera non è inizializzata. Per inizializzara invia: /activate_camera')
            return

        chat_id = update.effective_chat.id

        self.detector.detect()
        self.detector.check_free_spot()
        free_boxes = self.detector.free_boxes
        if free_boxes:
            update.message.reply_text(f"Posti liberi: {len(free_boxes)}")
        else:
            update.message.reply_text("Nessun posto libero")
        
        file_path = self.detector.situation_path
        update.message.reply_text("Ecco a te zio, questa è la situazione attuale del parcheggio:")
        try:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        except FileNotFoundError:
            update.message.reply_text('File non trovato.')
    
    def activate_camera(self, update: Update, context: CallbackContext) -> None:
        try:
            self.camera.activate()
            self.is_camera_active = True
            update.message.reply_text('Camera operativa')
        except Exception as e:
            print(e)
            update.message.reply_text('Inizializzazione della camera fallita')
            
        
    def deactivate_camera(self, update: Update, context: CallbackContext) -> None:
        try:
            self.camera.deactivate()
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
        
        attach_path = self.camera.take_snapshot()
        attach_path = attach_path if attach_path else "image.jpg"
        file_path = os.path.join(self.base_dir, 'media', attach_path)
        update.message.reply_text("Ecco a te zio, questa è la situazione attuale del parcheggio:")
        try:
            with open(file_path, 'rb') as file:
                context.bot.send_document(chat_id=chat_id, document=file)
        except FileNotFoundError:
            update.message.reply_text('File non trovato.')

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
        print("Bot started")
        
