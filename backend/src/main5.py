from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

from flask import Flask, request, jsonify
import threading
import logging

from bot.oauth_service import gen_oauth_link, store_state, get_user_id, get_token
from config.load_env import bot_token


# set logging for the bot
logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s  - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# /connect command handler
async def connect_command(update: Update, context: CallbackContext):
    
    oauth_link, state = gen_oauth_link()  # generate oauth link
    store_state(update.effective_user.id, state) # store the state in Redis along with user_id mapping
    logger.info(f"user - {update.effective_user.id}, state - {state}")
    await update.message.reply_text(f"Connect to Asana:\n\n{oauth_link}") #send oauth link to the user


# OAuth callback route
app = Flask(__name__)

@app.route('/callback', methods=['GET'])

def callback():
    auth_code = request.args.get('code')
    res_state = request.args.get('state')
    
    logger.info(f"recieved callback, state - {res_state}")
    user_id = get_user_id(res_state) # fetch the user_id associated with the state
    
    if not user_id:
        logger.error(f"invalid/expired state - {res_state}")
        return "Invalid / Expired state", 400
    
    logger.info(f"valid state for user - {user_id}")
    
    access_token = get_token(auth_code) # Exchange auth code for access token

    if access_token:
        logger.info(f"got access_token for user - {user_id}")
        return jsonify({"message": "Authorization successful", "access_token": access_token})
    else:
        logger.error(f"error exchanging code for user - {user_id}")
        return "Error exchanging code", 400


# run flask app in a separate thread to handle OAuth callback
def start_flask_app():
    app.run(port=5000, debug=True, use_reloader=False)


# run bot
def main():
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("connect", connect_command)) # add /connect command handler
    application.run_polling()


if __name__ == "__main__":
    threading.Thread(target=start_flask_app).start() # run flask in sep. thread
    main() 
    
    