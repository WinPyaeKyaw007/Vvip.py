from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Admin ID (Telegram မှာ @userinfobot နဲ့ ရနိုင်)
ADMIN_ID = 1794465007  # Admin ရဲ့ ID ကိုဒီမှာထည့်ပေးပါ

# Bot ကို Start လုပ်သော User တွေကိုသိမ်းထားမယ်
started_users = set()

# Start command ကို handle လုပ်မယ့် function
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username if user.username else user.id  # Username ရှိရင်သုံးမယ်၊ မရှိရင် User ID သုံးမယ်
    started_users.add(username)  # User ကို started_users list ထဲထည့်မယ်
    welcome_msg = """
    Hight Quality Vip Bot ပါရှင့် Botဖြစ်တဲ့အတွက်စာပြန်ပို့လို့မရနိုင်ပါရှင့်  
    Videoလေးတွေကို မကြာမကြာသလို ဒီBotလေးကနေပို့ပေးနေမှာပါရှင့်  
    Update အသစ်လေးတွေကိုလဲစောင့်မျော်ပေးကြပါအုံးရှင့်
    """
    update.message.reply_text(welcome_msg)

# Admin ကို Bot ကို Start လုပ်သော User အရေအတွက်ပြတာ
def start_count(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        count = len(started_users)
        update.message.reply_text(f"Bot ကို start လုပ်ခဲ့တဲ့ user အရေအတွက်: {count}")
    else:
        update.message.reply_text("You're not authorized to use this command.")

# Admin က user တွေကို မက်ဆေ့့ပို့နိုင်တဲ့ command
def broadcast(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        message = " ".join(context.args)  # Command ပြီးနောက်တွင် ပေးပို့လိုသော message
        for user in started_users:
            context.bot.send_message(chat_id=user, text=message)
    else:
        update.message.reply_text("You're not authorized to use this command.")

# Admin က user ကို ban လုပ်နိုင်တဲ့ command
def ban(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        user_to_ban = context.args[0]  # Ban လုပ်ချင်တဲ့ Username
        if user_to_ban in started_users:
            started_users.remove(user_to_ban)
            update.message.reply_text(f"{user_to_ban} has been banned.")
        else:
            update.message.reply_text(f"{user_to_ban} is not in the list.")
    else:
        update.message.reply_text("You're not authorized to use this command.")

# Admin က user ကို unban လုပ်နိုင်တဲ့ command
def unban(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        user_to_unban = context.args[0]
        started_users.add(user_to_unban)
        update.message.reply_text(f"{user_to_unban} has been unbanned.")
    else:
        update.message.reply_text("You're not authorized to use this command.")

# Admin က user ရဲ့ username link ကိုသိနိုင်တဲ့ command
def user_link(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        user = update.message.reply_to_message.from_user
        if user.username:
            update.message.reply_text(f"User's username link: @{user.username}")
        else:
            update.message.reply_text("This user doesn't have a username.")
    else:
        update.message.reply_text("You're not authorized to use this command.")

# Bot ကို run ဖို့ main function
def main():
    updater = Updater("7509251415:AAEW2B-TOwHUF7aQmez1fr_6pf6oil7me8M", use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers တွေကို add လုပ်ပေးတာ
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("start_count", start_count))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))
    dispatcher.add_handler(CommandHandler("ban", ban, pass_args=True))
    dispatcher.add_handler(CommandHandler("unban", unban, pass_args=True))
    dispatcher.add_handler(CommandHandler("user_link", user_link))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
