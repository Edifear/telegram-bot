import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Google Sheet setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "your_credentials.json"  # Path to your service account JSON
SPREADSHEET_NAME = "Your Google Sheet Name"

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
gc = gspread.authorize(credentials)
sheet = gc.open(SPREADSHEET_NAME).sheet1

# Logging
logging.basicConfig(level=logging.INFO)

# /points command handler
async def points_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            await update.message.reply_text("Please provide a name: !points <name>")
            return

        name = ' '.join(context.args).strip().lower()
        data = sheet.get_all_records()

        for row in data:
            if row['name'].lower() == name:
                await update.message.reply_text(f"{name} has {row['points']} points.")
                return

        await update.message.reply_text(f"Name '{name}' not found.")
    except Exception as e:
        await update.message.reply_text("Error fetching data.")

# Main bot entry
if __name__ == '__main__':
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("points", points_handler))
    app.run_polling()