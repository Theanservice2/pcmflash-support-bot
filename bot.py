import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    CallbackQueryHandler, 
    ChatMemberHandler, 
    ContextTypes
)

# ==========================================
# 1. ការកំណត់ទិន្នន័យ (CONFIGURATION)
# ==========================================
BOT_TOKEN = "8847902346:AAFwOzl9LFSRz3RvgYidUHqtZ6PJ4Frclco"
VDO_GROUP_ID = -1003725492397       # Group Hosting វីដេអូ
TEACHER_CHAT_ID = 1580528932        # Chat ID លោកគ្រូ

# 🔗 Link Group ធំដោះស្រាយបញ្ហារបស់លោកគ្រូ
GROUP_CHAT_URL = "https://t.me/+ZGwBn2H6nFs5Mzk1"

# 🆔 ID Group ធំសម្រាប់ឱ្យ Bot ផ្ញើសារ Alert
MAIN_GROUP_CHAT_ID = -1001846334558

# ==========================================
# 2. បញ្ជីមេរៀន (AUTO-FILL LESSONS LIST)
# ==========================================
LESSONS = [
    {
        "title": "📹 Techstream របស់ខ្ញុំត្រូវការ Key License",
        "msg_id": 3,
        "id": "vdo_lesson_1"
    },
    {
        "title": "📹 Techstream មិនស្គាល់ខ្សែស្កេន",
        "msg_id": 4,
        "id": "vdo_lesson_2"
    },
    {
        "title": "📄 មេរៀនលម្អិតពីការបិទកូដ ការយកហ្វាល់ទៅកែនិងរ៉ាយហ្វាល់",
        "msg_id": 43,
        "id": "vdo_lesson_3"
    },
    {
        "title": "📹 មេរៀនបិទកូដឡានទូទៅពីដើមដល់ចប់",
        "msg_id": 126,
        "id": "vdo_lesson_4"
    },
    {
        "title": "📹 របៀបបិទកូដ Nx200t",
        "msg_id": 62,
        "id": "vdo_lesson_5"
    },
    {
        "title": "📹 របៀបប្រើកម្មវិធី Toyolex3",
        "msg_id": 63,
        "id": "vdo_lesson_6"
    },
    {
        "title": "📹 របៀបប្រើកម្មវិធី Xdecoder (កែកូដ Nissan)",
        "msg_id": 64,
        "id": "vdo_lesson_7"
    },
    {
        "title": "📹 របៀបប្រើកម្មវិធី Toyolex4 (បិទឈីបសោរ)",
        "msg_id": 65,
        "id": "vdo_lesson_8"
    },   
    {
        "title": "📹 របៀបមើលលេខកូដដែលត្រូវ Update file",
        "msg_id": 128,
        "id": "vdo_lesson_9"
    },   
    {
        "title": "📹 របៀប Update file (CUW)",
        "msg_id": 129,
        "id": "vdo_lesson_10"
    },  
]

# Logging Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==========================================
# 3. MENU ចម្បង (AUTO-FILL KEYBOARD)
# ==========================================
def get_main_menu_keyboard():
    keyboard = []
    
    for lesson in LESSONS:
        keyboard.append([InlineKeyboardButton(lesson["title"], callback_data=lesson["id"])])
    
    keyboard.append([
        InlineKeyboardButton("❓ សំណួរញឹកញាប់ (FAQ)", callback_data="faq_menu"),
        InlineKeyboardButton("💬 ផ្ញើសារទៅលោកគ្រូ", callback_data="contact_teacher")
    ])
    
    return InlineKeyboardMarkup(keyboard)

# ==========================================
# 4. HANDLERS (ការឆ្លើយតបរបស់ BOT)
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "សួស្ដី! ខ្ញុំជា Support Bot របស់ <b>Theanservice</b> សម្រាប់ថ្នាក់រៀន PCM Flash។\n\n"
        "សូមជ្រើសរើសមេរៀន ឬសេវាកម្មដែលអ្នកត្រូវការខាងក្រោម៖"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")

# ------------------------------------------
# មុខងារស្វាគមន៍សមាជិកថ្មី (AUTO WELCOME)
# ------------------------------------------
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    
    # ត្រួតពិនិត្យថាតើមាន Member ថ្មីចូល (Joined) ឬត្រូវគេ Add ចូល Group
    if result.old_chat_member.status in ["left", "kicked"] and result.new_chat_member.status in ["member", "administrator"]:
        new_user = result.new_chat_member.user
        
        # កុំស្វាគមន៍ Bot ផ្សេងៗ
        if new_user.is_bot:
            return
            
        user_id = new_user.id
        user_name = html.escape(new_user.full_name)
        username = new_user.username
        
        if username:
            user_mention = f"@{username}"
        else:
            user_mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
            
        bot_username = (await context.bot.get_me()).username
        
        welcome_msg = (
            f"🎉 <b>សូមស្វាគមន៍បង {user_mention}</b> ដែលជាសមាជិកថ្មីនៃគ្រុបនេះ!\n\n"
            f"ខាងក្រោមនេះគឺជាជំនួយការដ៏ឆ្លាតវៃក្នុងការជួយដោះស្រាយរាល់បញ្ហាដែលបងជួបប្រទះបានយ៉ាងឆាប់រហ័ស។ "
            f"សូមចុចប៊ូតុងខាងក្រោមដើម្បីបើកប្រព័ន្ធ Support ផ្ទាល់ខ្លួន៖"
        )
        
        bot_btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 បើក @TheanserviceSupport_bot", url=f"https://t.me/{bot_username}?start=menu")]
        ])
        
        try:
            await context.bot.send_message(
                chat_id=result.chat.id,
                text=welcome_msg,
                reply_markup=bot_btn,
                parse_mode="HTML"
            )
            print(f"✅ បានផ្ញើសារស្វាគមន៍ទៅកាន់សមាជិកថ្មី {new_user.full_name}")
        except Exception as e:
            print(f"❌ កំហុសក្នុងការផ្ញើសារ Auto Welcome: {e}")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_name = html.escape(query.from_user.full_name)
    username = query.from_user.username
    
    if username:
        user_mention = f"@{username}"
    else:
        user_mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
        
    data = query.data

    # --- ត្រួតពិនិត្យ និង ផ្ញើ VDO តាម AUTO-FILL LIST ---
    for lesson in LESSONS:
        if data == lesson["id"]:
            await query.message.reply_text("⏳ កំពុងទាញយកមេរៀនជូន...")
            try:
                await context.bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=VDO_GROUP_ID,
                    message_id=lesson["msg_id"]
                )
            except Exception as e:
                await query.message.reply_text("⚠️ មិនអាចទាញយក VDO បានទេ! សូមពិនិត្យមើលថាតើ Bot ជា Admin ក្នុង Group ឬនៅ?")
            return

    # --- ផ្នែក FAQ (សំណួរញឹកញាប់) ---
    if data == "faq_menu":
        faq_keyboard = [
            [InlineKeyboardButton("⚠️ របៀបដោះស្រាយ Error Identification / Read / Write (PCM Flash):", callback_data="faq_err_rw")],
            [InlineKeyboardButton("🔌 ប្រភេទ Hardware ដែលគាំទ្រគឺ J2534.....", callback_data="faq_hardware")],
            [InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data="back_to_main")]
        ]
        await query.message.reply_text("ជម្រើសសំណួរញឹកញាប់ (FAQ)៖", reply_markup=InlineKeyboardMarkup(faq_keyboard))

    elif data == "faq_err_rw":
        faq_text = (
            "💡 <b>ការដោះស្រាយបញ្ហា Error Identification / Read / Write (PCM Flash):</b>\n\n"
            "១. ពិនិត្យមើលភ្លើងនិងម៉ាស់ 12V / 13.8V សព្វគ្រប់ដែរឬទេ (បើធ្វើលើឡានកុំភ្លេចគូសបន្ថែម)\n"
            "២. ពិនិត្យមើល USB Mongose JLR or Openport2\n"
            "៣. ពិនិត្យមើល Pinout BATT / IGWS & B+ / Can-High / Can-Low ថាបានតត្រូវតាម Diagram ឬនៅ"
        )
        await query.message.reply_text(faq_text, parse_mode="HTML")

    elif data == "faq_hardware":
        faq_hw_text = (
            "💡 <b>Hardware ដែលគាំទ្រការងារ PCM Flash៖</b>\n\n"
            "• PCM Flash USB Dongle (License)\n"
            "• Mongoose JLR\n"
            "• Tactrix OpenPort 2.0\n"
            "• Scanmatik 2 or 3 Pro\n"
            "• Any J2534 Devices"
        )
        await query.message.reply_text(faq_hw_text, parse_mode="HTML")

    elif data == "back_to_main":
        await query.message.reply_text(
            "សូមជ្រើសរើសមេរៀន ឬសេវាកម្មដែលអ្នកត្រូវការខាងក្រោម៖",
            reply_markup=get_main_menu_keyboard()
        )

    # --- ផ្នែកទាក់ទងលោកគ្រូ (ផ្ញើ Link ចូល Group ធំ + ផ្ញើសារ Alert ចូល Group ធំ) ---
    elif data == "contact_teacher":
        group_btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 ចូលទៅកាន់ Group ដោះស្រាយបញ្ហាធំ", url=GROUP_CHAT_URL)]
        ])
        await query.message.reply_text(
            "លោកគ្រូបានទទួលការជូនដំណឹងហើយ! សូមចុចប៊ូតុងខាងក្រោមដើម្បីចូលទៅកាន់ Group ធំ និងផ្ញើសារសួរដោះស្រាយបញ្ហាផ្ទាល់ជាមួយលោកគ្រូ៖",
            reply_markup=group_btn
        )
        
        # ផ្ញើសារ Alert ស្វ័យប្រវត្តិ ចូលទៅកាន់ Group ធំ (ប្រើ HTML Mode ដើម្បីការពារ Error)
        try:
            group_alert_msg = (
                f"🚨 <b>សិស្សត្រូវការជំនួយ!</b>\n\n"
                f"សួស្ដីលោកគ្រូ! ខ្ញុំបាទ {user_mention} កំពុងមានបញ្ហាត្រូវការលោកគ្រូជួយដោះស្រាយជាបន្ទាន់ "
                f"ពីព្រោះខ្ញុំបានព្យាយាមតាមរយៈការណែនាំរបស់ @TheanserviceSupport_bot រួចមកហើយប៉ុន្តែនៅតែមិនអាចដោះស្រាយបញ្ហារបស់ខ្ញុំបាន។"
            )
            await context.bot.send_message(
                chat_id=MAIN_GROUP_CHAT_ID,
                text=group_alert_msg,
                parse_mode="HTML"
            )
            print("✅ ផ្ញើសារ Alert ចូល Group ធំបានជោគជ័យ!")
        except Exception as e:
            print(f"❌ កំហុសក្នុងការផ្ញើសារចូល Group ធំ៖ {e}")

        # ផ្ញើសារ Alert ជូនលោកគ្រូក្នុងឆាតផ្ទាល់ខ្លួន
        try:
            alert_msg = (
                f"🔔 <b>សិស្សសួររក Support!</b>\n\n"
                f"👤 ឈ្មោះ: {user_mention} (ID: <code>{user_id}</code>)\n"
                f"បានចុចប៊ូតុងទាក់ទងលោកគ្រូ ហើយ Bot បានផ្ញើសារជូនដំណឹងចូល Group ធំរួចរាល់។"
            )
            await context.bot.send_message(
                chat_id=TEACHER_CHAT_ID,
                text=alert_msg,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"❌ កំហុសក្នុងការផ្ញើសារជូនលោកគ្រូ៖ {e}")

# ==========================================
# 5. កំណត់ MENU BAR ជាប់លើ TELEGRAM
# ==========================================
async def post_init(application):
    commands = [
        BotCommand("start", "start / ចាប់ផ្ដើម")
    ]
    await application.bot.set_my_commands(commands)

# ==========================================
# 6. START BOT SERVER
# ==========================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    # បន្ថែម Handler ចាប់យកការចូលរបស់សមាជិកថ្មី
    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))

    print("🚀 Bot @TheanserviceSupport_bot កំពុងដំណើរការ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()