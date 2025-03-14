from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

# وضعیت‌های مختلف در مکالمه
CHOOSING, TYPING_AMOUNT, TYPING_TEAM_NAME, TYPING_RESULT, TYPING_NAME, TYPING_PHONE = range(6)

# شروع ربات
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("سایت راسان دیزاین", url="http://rasandesign.github.io/ir/"),  # لینک وبسایت خودتان را وارد کنید
        ],
        [
            InlineKeyboardButton("معرفی خود", callback_data='place_bet'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('سلام! خوش آمدید، انتخاب کنید این سوالات فقط جهت شرکت در اسکیود گیم راسان دیزاین است . اگر اشتباه پر کنید شرکت داده نمیشوید  :', reply_markup=reply_markup)

# گزینه "گذاشتن شرط"
async def place_bet(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("بازگشت", callback_data='cancel')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # استفاده از update.callback_query.message به جای update.message
    await update.callback_query.message.reply_text("نام پدر را وارد کنید:", reply_markup=reply_markup)
    return TYPING_AMOUNT

# گرفتن مقدار شرط
async def typing_amount(update: Update, context: CallbackContext) -> int:
    context.user_data['amount'] = update.message.text  # مقدار شرط را ذخیره می‌کنیم
    await update.message.reply_text("تاریخ تولد خود را وارد کنید:")
    return TYPING_TEAM_NAME

# گرفتن نام تیم‌ها و نتیجه
async def typing_team_name(update: Update, context: CallbackContext) -> int:
    context.user_data['team_names'] = update.message.text  # نام تیم‌ها و نتیجه را ذخیره می‌کنیم
    await update.message.reply_text("نام خود را وارد کنید:")
    return TYPING_NAME

# گرفتن نام کاربر
async def typing_name(update: Update, context: CallbackContext) -> int:
    context.user_data['user_name'] = update.message.text  # نام کاربر را ذخیره می‌کنیم
    await update.message.reply_text("شماره تماس خود را وارد کنید:")
    return TYPING_PHONE

# گرفتن شماره تماس
async def typing_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone_number'] = update.message.text  # شماره تماس را ذخیره می‌کنیم
    # ارسال اطلاعات به کانال F6RSi.t.me
    message = f"""
    نام پدر: {context.user_data['amount']} 
    تاریخ تولد: {context.user_data['team_names']}
    نام کاربر: {context.user_data['user_name']}
    شماره تماس: {context.user_data['phone_number']}
    """
    # ارسال پیام به کانال تلگرام
    await context.bot.send_message(chat_id="@Ropals", text=message)
    await update.message.reply_text("شرط شما ثبت شد!")
    return ConversationHandler.END

# بازگشت از فرآیند
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END

# تابع اصلی برای راه‌اندازی ربات
def main() -> None:
    # ایجاد برنامه
    application = Application.builder().token("7851763243:AAEAaOb3_Z_19c90NnG0SFgB_kXjvmehdJo").build()

    # تعریف دستور start
    application.add_handler(CommandHandler("start", start))

    # تعریف ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(place_bet, pattern='^place_bet$')],
        states={
            TYPING_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_amount)],
            TYPING_TEAM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_team_name)],
            TYPING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_name)],
            TYPING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_phone)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel$')],
    )

    # افزودن handler به برنامه
    application.add_handler(conv_handler)

    # اجرای ربات
    application.run_polling()

if __name__ == '__main__':
    main()
