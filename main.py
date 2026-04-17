import os
import logging
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, add_message, get_all_messages
from ai_features import ask_command, search_command, define_command, code_command, imagine_command, news_command, explain_command, summarize_command, grammar_command, story_command, poem_command, lyrics_command, essay_command, debate_command, eli5_command, aiagent_command, translate_command, detect_command
from features import dua_command, wisdom_command, quran_command, hadith_command, asmaulhusna_command, prayertime_command, note_command, notes_command, delnote_command, todo_command, todos_command, donetodo_command, remind_command, bookmark_command, bookmarks_command, calc_command, weather_command, qr_command, convert_command, currency_command, time_command, countdown_command, wordcount_command, base64_command, hash_command, shorten_command, password_command, color_command, emoji_command, reverse_command, upper_command, lower_command, quote_command, joke_command, fact_command, flip_command, roll_command, choose_command, rng_command, eightball_command, dare_command, truth_command, would_command, rate_command, ship_command, roast_command, compliment_command, me_command, afk_command, bio_command, setbio_command, level_command, poll_command, stats_command, rules_command, id_command, report_command, feedback_command, groupinfo_command, admin_command, mute_command, unmute_command, warn_command, unwarn_command, warns_command, pin_command, unpin_command, announce_command, tagall_command, setrules_command, addcmd_command, delcmd_command, slowmode_command, purge_command, settings_command, setlang_command, setnotif_command, book_command
import telegram # Added for ChatPermissions in mute/unmute

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "your-bot-token-here")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome = (
        f"\U0001f916 <b>Min Thu Bot V7</b>\n"
        f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        f"\u1019\u1004\u103a\u1039\u1002\u101c\u102c\u1015\u102b {user.mention_html()}!\n\n"
        f"\u1000\u103b\u103d\u1014\u103a\u1010\u1031\u102c\u103a\u1000 Min Thu Bot \u1015\u102b\u104b\n"
        f"AI, \u1018\u102c\u101e\u102c\u1015\u103c\u1014\u103a, Islamic, Tools, Fun \u1005\u1010\u1032\u1037 features \u1019\u103b\u102c\u1038\u1005\u103d\u102c \u1000\u1030\u100a\u102e\u1015\u1031\u1038\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u1010\u101a\u103a\u104b\n\n"
        f"\U0001f4cb /help - Commands \u1021\u102c\u1038\u101c\u102f\u1036\u1038 \u1000\u103c\u100a\u103a\u1037\u101b\u1014\u103a"
    )
    await update.message.reply_html(welcome)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "\U0001f916 <b>Min Thu Bot V7 - Commands</b>\n"
        "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        "\U0001f9e0 <b>AI & Search:</b>\n"
        "/ask, /search, /define, /code, /imagine, /news, /explain, /summarize, /grammar, /story, /poem, /lyrics, /essay, /debate, /eli5, /aiagent\n\n"
        "\U0001f30e <b>Translation:</b>\n"
        "/translate, /detect\n\n"
        "\U0001f54c <b>Islamic:</b>\n"
        "/dua, /wisdom, /quran, /hadith, /asmaulhusna, /prayertime\n\n"
        "\U0001f4dd <b>Notes & Tasks:</b>\n"
        "/note, /notes, /delnote, /todo, /todos, /donetodo, /remind, /bookmark, /bookmarks\n\n"
        "\U0001f527 <b>Tools:</b>\n"
        "/calc, /weather, /qr, /convert, /currency, /time, /countdown, /wordcount, /base64, /hash, /shorten, /password, /color, /emoji, /reverse, /upper, /lower\n\n"
        "\U0001f3b2 <b>Fun:</b>\n"
        "/quote, /joke, /fact, /flip, /roll, /choose, /rng, /8ball, /dare, /truth, /would, /rate, /ship, /roast, /compliment\n\n"
        "\U0001f464 <b>Profile:</b>\n"
        "/me, /afk, /bio, /setbio, /level\n\n"
        "\U0001f4ca <b>Group:</b>\n"
        "/poll, /stats, /rules, /id, /report, /feedback, /groupinfo\n\n"
        "\U0001f46e <b>Admin:</b>\n"
        "/admin, /mute, /unmute, /warn, /unwarn, /warns, /pin, /unpin, /announce, /tagall, /setrules, /addcmd, /delcmd, /slowmode, /purge\n\n"
        "\u2699\ufe0f <b>Settings:</b>\n"
        "/settings, /setlang, /setnotif\n\n"
        "\U0001f4da <b>Book Search:</b>\n"
        "/book [search query]\n\n"
        "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
        "\U0001f4a1 @minthu786bot \u1000\u102d\u102f tag \u101c\u102f\u1015\u103a\u1015\u103c\u102e\u1038\u101c\u100a\u103a\u1038 \u1019\u1031\u1038\u1014\u102d\u102f\u1004\u103a\u1015\u102b\u1010\u101a\u103a!"
    )
    await update.message.reply_html(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all non-command messages for duplicate detection and storage."""
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    text = update.message.text

    if not text: # Ignore non-text messages for now
        return

    # Store message in DB (all messages)
    add_message(chat_id, message_id, text)

    # Check for duplicate messages
    all_messages = get_all_messages()
    duplicate_found = False
    original_message_id = None

    for msg_chat_id, msg_message_id, msg_text in all_messages:
        if msg_chat_id == chat_id and msg_message_id != message_id and msg_text == text:
            duplicate_found = True
            original_message_id = msg_message_id
            break

    if duplicate_found:
        burmese_warning = "ဤသည်မှာ ထပ်နေသော မက်ဆေ့ချ်တစ်ခုဖြစ်သည်။ ကျေးဇူးပြု၍ မက်ဆေ့ချ်များကို ထပ်ခါတလဲလဲ မပို့ပါနှင့်။"
        await update.message.reply_text(
            burmese_warning,
            reply_to_message_id=original_message_id
        )
    # If not duplicate, silently store only

async def mention_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply when the bot is mentioned with AI response."""
    from ai_features import generate_text_response
    text = update.message.text or ""
    text = text.replace("@minthu786bot", "").strip()
    if text:
        response = await generate_text_response(text)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("\u1019\u1004\u103a\u1039\u1002\u101c\u102c\u1015\u102b! \u1000\u103b\u103d\u1014\u103a\u1010\u1031\u102c\u103a Min Thu Bot \u1015\u102b\u104b \u1018\u102c\u1000\u1030\u100a\u102e\u1015\u1031\u1038\u101b\u1019\u101c\u1032? \U0001f916")

def main() -> None:
    """Start the bot."""
    init_db() # Initialize the database

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # AI Commands
    application.add_handler(CommandHandler("ask", ask_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("define", define_command))
    application.add_handler(CommandHandler("code", code_command))
    application.add_handler(CommandHandler("imagine", imagine_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("explain", explain_command))
    application.add_handler(CommandHandler("summarize", summarize_command))
    application.add_handler(CommandHandler("grammar", grammar_command))
    application.add_handler(CommandHandler("story", story_command))
    application.add_handler(CommandHandler("poem", poem_command))
    application.add_handler(CommandHandler("lyrics", lyrics_command))
    application.add_handler(CommandHandler("essay", essay_command))
    application.add_handler(CommandHandler("debate", debate_command))
    application.add_handler(CommandHandler("eli5", eli5_command))
    application.add_handler(CommandHandler("aiagent", aiagent_command))

    # Other Commands (placeholders for now)
    application.add_handler(CommandHandler("translate", translate_command))
    application.add_handler(CommandHandler("detect", detect_command))
    application.add_handler(CommandHandler("dua", dua_command))
    application.add_handler(CommandHandler("wisdom", wisdom_command))
    application.add_handler(CommandHandler("quran", quran_command))
    application.add_handler(CommandHandler("hadith", hadith_command))
    application.add_handler(CommandHandler("asmaulhusna", asmaulhusna_command))
    application.add_handler(CommandHandler("prayertime", prayertime_command))
    application.add_handler(CommandHandler("note", note_command))
    application.add_handler(CommandHandler("notes", notes_command))
    application.add_handler(CommandHandler("delnote", delnote_command))
    application.add_handler(CommandHandler("todo", todo_command))
    application.add_handler(CommandHandler("todos", todos_command))
    application.add_handler(CommandHandler("donetodo", donetodo_command))
    application.add_handler(CommandHandler("remind", remind_command))
    application.add_handler(CommandHandler("bookmark", bookmark_command))
    application.add_handler(CommandHandler("bookmarks", bookmarks_command))
    application.add_handler(CommandHandler("calc", calc_command))
    application.add_handler(CommandHandler("weather", weather_command))
    application.add_handler(CommandHandler("qr", qr_command))
    application.add_handler(CommandHandler("convert", convert_command))
    application.add_handler(CommandHandler("currency", currency_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("countdown", countdown_command))
    application.add_handler(CommandHandler("wordcount", wordcount_command))
    application.add_handler(CommandHandler("base64", base64_command))
    application.add_handler(CommandHandler("hash", hash_command))
    application.add_handler(CommandHandler("shorten", shorten_command))
    application.add_handler(CommandHandler("password", password_command))
    application.add_handler(CommandHandler("color", color_command))
    application.add_handler(CommandHandler("emoji", emoji_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(CommandHandler("upper", upper_command))
    application.add_handler(CommandHandler("lower", lower_command))
    application.add_handler(CommandHandler("quote", quote_command))
    application.add_handler(CommandHandler("joke", joke_command))
    application.add_handler(CommandHandler("fact", fact_command))
    application.add_handler(CommandHandler("flip", flip_command))
    application.add_handler(CommandHandler("roll", roll_command))
    application.add_handler(CommandHandler("choose", choose_command))
    application.add_handler(CommandHandler("rng", rng_command))
    application.add_handler(CommandHandler("8ball", eightball_command))
    application.add_handler(CommandHandler("dare", dare_command))
    application.add_handler(CommandHandler("truth", truth_command))
    application.add_handler(CommandHandler("would", would_command))
    application.add_handler(CommandHandler("rate", rate_command))
    application.add_handler(CommandHandler("ship", ship_command))
    application.add_handler(CommandHandler("roast", roast_command))
    application.add_handler(CommandHandler("compliment", compliment_command))
    application.add_handler(CommandHandler("me", me_command))
    application.add_handler(CommandHandler("afk", afk_command))
    application.add_handler(CommandHandler("bio", bio_command))
    application.add_handler(CommandHandler("setbio", setbio_command))
    application.add_handler(CommandHandler("level", level_command))
    application.add_handler(CommandHandler("poll", poll_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("groupinfo", groupinfo_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("mute", mute_command))
    application.add_handler(CommandHandler("unmute", unmute_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("unwarn", unwarn_command))
    application.add_handler(CommandHandler("warns", warns_command))
    application.add_handler(CommandHandler("pin", pin_command))
    application.add_handler(CommandHandler("unpin", unpin_command))
    application.add_handler(CommandHandler("announce", announce_command))
    application.add_handler(CommandHandler("tagall", tagall_command))
    application.add_handler(CommandHandler("setrules", setrules_command))
    application.add_handler(CommandHandler("addcmd", addcmd_command))
    application.add_handler(CommandHandler("delcmd", delcmd_command))
    application.add_handler(CommandHandler("slowmode", slowmode_command))
    application.add_handler(CommandHandler("purge", purge_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("setlang", setlang_command))
    application.add_handler(CommandHandler("setnotif", setnotif_command))
    application.add_handler(CommandHandler("book", book_command))

    # Handle messages that mention the bot
    application.add_handler(MessageHandler(filters.Regex(r'@minthu786bot'), mention_reply))

    # On non command i.e. message - handle it for duplicate detection and storage
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
