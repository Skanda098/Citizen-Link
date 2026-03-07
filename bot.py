import telebot
import sqlite3
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Securely fetch keys
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Missing API Keys! Check your .env file.")

bot = telebot.TeleBot(BOT_TOKEN)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to CivicSnap! Please send a photo of the civic issue (Pothole or Garbage).")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    image_filename = f"static/uploads/{chat_id}_{message.message_id}.jpg"
    with open(image_filename, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    processing_msg = bot.reply_to(message, "🔍 AI is analyzing your image...")
    
    try:
        img = Image.open(image_filename)
        prompt = "Look at this image. Is it a public pothole, public garbage, or neither? Reply with EXACTLY one word: Pothole, Garbage, or Gibberish."
        
        response = model.generate_content([prompt, img])
        result_text = response.text.strip().lower()
        
        print(f"Raw AI Output: {result_text}") 
        
        if "pothole" in result_text:
            category = "Pothole"
        elif "garbage" in result_text:
            category = "Garbage"
        else:
            category = "Gibberish"
            
    except Exception as e:
        print(f"AI CRASHED: {e}")
        bot.delete_message(chat_id, processing_msg.message_id)
        bot.send_message(chat_id, f"❌ **System Error:** The AI connection failed. Error details: {e}")
        return

    bot.delete_message(chat_id, processing_msg.message_id)
    
    if category == "Gibberish":
        bot.send_message(chat_id, "🛑 **AI Triage Rejected:**\nThis image does not appear to be a valid civic issue. Please submit a clear photo of a pothole or garbage.")
        os.remove(image_filename)
        return

    user_data[chat_id] = {'image': image_filename, 'category': category}
    bot.send_message(chat_id, f"✅ **AI Triage:** Identified as '{category}'.\n\nNow, tap the attachment icon (📎) and share your **Location**.")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    
    if chat_id not in user_data or 'image' not in user_data[chat_id]:
        bot.reply_to(message, "Please send a valid photo first.")
        return

    lat = message.location.latitude
    lon = message.location.longitude
    image_path = user_data[chat_id]['image']
    category = user_data[chat_id]['category'] 
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO issues (user_id, category, latitude, longitude, image_path, status) VALUES (?, ?, ?, ?, ?, ?)",
              (chat_id, category, lat, lon, image_path, "Reported"))
    
    issue_id = c.lastrowid 
    
    conn.commit()
    conn.close()
    
    del user_data[chat_id]
    
    bot.reply_to(message, f"📍 Issue #{issue_id} successfully mapped on the dashboard!")

print("AI Gatekeeper Bot is polling securely...")
bot.infinity_polling()