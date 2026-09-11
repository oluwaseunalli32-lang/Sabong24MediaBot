import os
import logging

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# ---------- Config ----------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------- Texts (Khmer) ----------
START_TEXT = (
    "សូមស្វាគមន៍មកកាន់ <b>មេបក្សីធំ - Sabong24</b> 🐓\n\n"
    "ខ្ញុំជាបូតព័ត៌មានអប់រំ ដែលផ្តល់ចំណេះដឹងអំពី៖\n"
    "• ប្រវត្តិ និងវប្បធម៌នៃសាប៊ុង (Sabong)\n"
    "• ពាក្យបច្ចេកទេសដែលគេប្រើក្នុងវិស័យចិញ្ចឹមមាន់\n"
    "• អត្ថបទអប់រំអំពីការចិញ្ចឹម ការថែទាំ និងសុខភាពសត្វ\n\n"
    "គោលបំណងរបស់ខ្ញុំគឺ <b>ការផ្តល់ព័ត៌មាន និងការអប់រំ</b> តែប៉ុណ្ណោះ។\n"
    "ខ្ញុំមិនផ្តល់សេវាភ្នាល់ ឬសកម្មភាពណាមួយដែលពាក់ព័ន្ធនឹងការភ្នាល់ឡើយ។\n\n"
    "សូមចុចប៊ូតុងខាងក្រោមដើម្បីចាប់ផ្តើមស្វែងយល់។"
)

GUIDE_MENU_TEXT = (
    "<b>📚 Sabong Guide</b>\n\n"
    "សូមជ្រើសរើសប្រធានបទដែលអ្នកចង់អាន៖"
)

WHAT_IS_TEXT = (
    "<b>🐓 តើសាប៊ុងជាអ្វី?</b>\n\n"
    "សាប៊ុង (Sabong) គឺជាទំនៀមទម្លាប់ប្រពៃណីមួយដែលមានប្រវត្តិយូរលង់ "
    "នៅក្នុងតំបន់អាស៊ីអាគ្នេយ៍ ជាពិសេសនៅក្នុងប្រទេសហ្វីលីពីន។ "
    "វាត្រូវបានចាត់ទុកជាផ្នែកមួយនៃវប្បធម៌ និងប្រពៃណីរបស់ប្រជាជន។\n\n"
    "<b>ប្រវត្តិសង្ខេប</b>\n"
    "• មានដើមកំណើតនៅអាស៊ីអាគ្នេយ៍ជាច្រើនសតវត្សមកហើយ\n"
    "• ត្រូវបានកត់ត្រាដោយអ្នកធ្វើដំណើរជនជាតិអឺរ៉ុបក្នុងសតវត្សទី 16\n"
    "• នៅប្រទេសហ្វីលីពីន វាត្រូវបានគេស្គាល់ជាទូទៅថា <b>Sabong</b>\n\n"
    "<b>ចំណាំ</b>\n"
    "ខ្លឹមសារនេះគឺសម្រាប់ការសិក្សា និងការយល់ដឹងអំពីវប្បធម៌តែប៉ុណ្ណោះ។ "
    "ខ្ញុំមិនលើកទឹកចិត្ត ឬផ្តល់សេវាទាក់ទងនឹងការភ្នាល់ឡើយ។"
)

TERMS_TEXT = (
    "<b>📖 ពាក្យបច្ចេកទេសសាប៊ុង</b>\n\n"
    "• <b>Sabong</b> — ពិធីប្រកួតមាន់ (ជាពាក្យហ្វីលីពីន)\n"
    "• <b>Manok</b> — មាន់\n"
    "• <b>Bulik</b> — មាន់ពូជមួយដែលមានពណ៌ចម្រុះ\n"
    "• <b>Hapon</b> — ពូជមាន់ដើមកំណើតជប៉ុន\n"
    "• <b>Kelso</b> — ពូជមាន់ដែលមានឈ្មោះល្បី\n"
    "• <b>Roundhead</b> — ពូជមាន់ដែលមានក្បាលមូល\n"
    "• <b>Sweater</b> — ពូជមាន់ដែលមានរោមវែង\n"
    "• <b>Breeder</b> — អ្នកចិញ្ចឹម និងបង្កាត់ពូជ\n"
    "• <b>Gamefowl</b> — មាន់ដែលគេចិញ្ចឹមសម្រាប់ពូជ\n"
    "• <b>Conditioning</b> — ការហ្វឹកហាត់ និងថែទាំសុខភាពមាន់"
)

ARTICLES_TEXT = (
    "<b>📚 អត្ថបទអប់រំ</b>\n\n"
    "<b>១. ប្រវត្តិនៃសាប៊ុងនៅអាស៊ីអាគ្នេយ៍</b>\n"
    "សាប៊ុងមានឫសគល់ពីប្រពៃណីកសិកម្ម និងការចិញ្ចឹមសត្វក្នុងគ្រួសារ។ "
    "តាមរយៈប្រវត្តិសាស្ត្រ វាបានក្លាយជាផ្នែកមួយនៃពិធីបុណ្យ និងការជួបជុំសហគមន៍។\n\n"
    "<b>២. ការចិញ្ចឹម និងការថែទាំមាន់</b>\n"
    "មាន់ត្រូវការអាហារដែលមានជីវជាតិ ទឹកស្អាត ទីជម្រកដែលមានខ្យល់ចេញចូល និងការថែទាំសុខភាពជាប្រចាំ។ "
    "ការយល់ដឹងអំពីជីវវិទ្យារបស់សត្វជួយឱ្យការចិញ្ចឹមមានប្រសិទ្ធភាព។\n\n"
    "<b>៣. ពូជមាន់ដែលពេញនិយម</b>\n"
    "មានពូជជាច្រើនដូចជា Hapon, Kelso, Roundhead និង Sweater។ "
    "ពូជនីមួយៗមានលក្ខណៈខុសៗគ្នាទាក់ទងនឹងទម្រង់ខ្លួន និងចរិត។\n\n"
    "<b>៤. សុខភាពសត្វ និងការការពារជំងឺ</b>\n"
    "ការចាក់វ៉ាក់សាំង ការសម្អាតទីជម្រក និងការឃ្លាំមើលសុខភាពជាប្រចាំ "
    "ជួយការពារជំងឺឆ្លងក្នុងហ្វូងសត្វ។"
)


# ---------- Keyboards ----------
def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("📚 Sabong Guide", callback_data="guide")]]
    )


def guide_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🐓 តើសាប៊ុងជាអ្វី?", callback_data="what_is")],
            [InlineKeyboardButton("📖 ពាក្យបច្ចេកទេសសាប៊ុង", callback_data="terms")],
            [InlineKeyboardButton("📚 អត្ថបទអប់រំ", callback_data="articles")],
            [InlineKeyboardButton("🔙 ត្រឡប់ក្រោយ", callback_data="main")],
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 ត្រឡប់ទៅ Sabong Guide", callback_data="guide")],
            [InlineKeyboardButton("🏠 ទំព័រដើម", callback_data="main")],
        ]
    )


# ---------- Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        START_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "ប្រើ /start ដើម្បីបើកម៉ឺនុយចម្បង។\n"
        "បូតនេះផ្តល់តែព័ត៌មានអប់រំប៉ុណ្ណោះ។",
        parse_mode=ParseMode.HTML,
    )


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text(
            START_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard(),
        )
    elif data == "guide":
        await query.edit_message_text(
            GUIDE_MENU_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=guide_keyboard(),
        )
    elif data == "what_is":
        await query.edit_message_text(
            WHAT_IS_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
    elif data == "terms":
        await query.edit_message_text(
            TERMS_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )
    elif data == "articles":
        await query.edit_message_text(
            ARTICLES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard(),
        )


# ---------- Entrypoint ----------
def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Please set it in your environment.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(on_callback))

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
