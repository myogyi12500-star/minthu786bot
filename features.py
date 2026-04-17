import random
import asyncio
import datetime
import hashlib
import base64
import qrcode
import io
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ContextTypes
from database import add_note, get_notes, delete_note, add_todo, get_todos, mark_todo_done, add_bookmark, get_bookmarks, get_user_profile, create_or_update_user_profile, set_afk_status, get_afk_status, add_warning, get_warnings, remove_last_warning, set_rules, get_rules, add_custom_command, get_custom_command, delete_custom_command, get_chat_settings, update_chat_settings
from ai_features import generate_text_response

# --- Islamic Commands ---
async def dua_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a short, meaningful Islamic Dua (supplication) in English and Arabic."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def wisdom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a short, insightful piece of Islamic wisdom or a quote from a prominent Islamic scholar."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def quran_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /quran [surah:ayah] (e.g., 1:1)")
        return
    
    query = context.args[0]
    try:
        surah, ayah = map(int, query.split(":"))
        url = f"http://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.asad"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200 and data["status"] == "OK":
                    ayah_text = data["data"]["text"]
                    surah_name = data["data"]["surah"]["englishName"]
                    await update.message.reply_text(f"Quran {surah_name} ({surah}:{ayah}):\n{ayah_text}")
                else:
                    await update.message.reply_text("Could not fetch Quran ayah. Please check the surah and ayah numbers.")
    except ValueError:
        await update.message.reply_text("Invalid format. Usage: /quran [surah:ayah] (e.g., 1:1)")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def hadith_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a short, authentic Hadith (saying of Prophet Muhammad) in English and Arabic."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def asmaulhusna_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This can be expanded to fetch from an API or a predefined list
    names = [
        "Ar-Rahman (The Most Merciful)", "Ar-Rahim (The Especially Merciful)",
        "Al-Malik (The King)", "Al-Quddus (The Holy)", "As-Salam (The Source of Peace)",
        "Al-Mu'min (The Giver of Faith)", "Al-Muhaymin (The Guardian)", "Al-Aziz (The Almighty)",
        "Al-Jabbar (The Compeller)", "Al-Mutakabbir (The Supreme)"
    ]
    await update.message.reply_text(f"One of the 99 Names of Allah: {random.choice(names)}")

async def prayertime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /prayertime [city]")
        return
    
    city = " ".join(context.args)
    # Using Aladhan API for prayer times
    # Example: http://api.aladhan.com/v1/timingsByCity?city=London&country=UK&method=2
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country=auto&method=2"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200 and data["status"] == "OK":
                timings = data["data"]["timings"]
                prayer_times_msg = f"Prayer times for {city.title()}:\n"
                fajr = timings['Fajr']
                sunrise = timings['Sunrise']
                dhuhr = timings['Dhuhr']
                asr = timings['Asr']
                maghrib = timings['Maghrib']
                isha = timings['Isha']
                prayer_times_msg += f"Fajr: {fajr}\n"
                prayer_times_msg += f"Sunrise: {sunrise}\n"
                prayer_times_msg += f"Dhuhr: {dhuhr}\n"
                prayer_times_msg += f"Asr: {asr}\n"
                prayer_times_msg += f"Maghrib: {maghrib}\n"
                prayer_times_msg += f"Isha: {isha}"
                await update.message.reply_text(prayer_times_msg)
            else:
                await update.message.reply_text(f"Could not fetch prayer times for {city}. Please check the city name.")

# --- Notes & Tasks Commands ---
async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /note [name] [content]")
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    note_name = context.args[0]
    note_content = " ".join(context.args[1:])

    if add_note(user_id, chat_id, note_name, note_content):
        await update.message.reply_text(f"Note ‘{note_name}’ saved.")
    else:
        await update.message.reply_text(f"Note ‘{note_name}’ already exists. Choose a different name.")

async def notes_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    notes = get_notes(user_id, chat_id)

    if notes:
        notes_list = "Your notes:\n"
        for name, content in notes:
            notes_list += f"- **{name}**: {content}\n"
        await update.message.reply_text(notes_list, parse_mode="Markdown")
    else:
        await update.message.reply_text("You have no notes.")

async def delnote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /delnote [name]")
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    note_name = context.args[0]

    if delete_note(user_id, chat_id, note_name):
        await update.message.reply_text(f"Note ‘{note_name}’ deleted.")
    else:
        await update.message.reply_text(f"Note ‘{note_name}’ not found.")

async def todo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /todo [task]")
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    task = " ".join(context.args)

    todo_id = add_todo(user_id, chat_id, task)
    await update.message.reply_text(f"Todo added with ID: {todo_id}")

async def todos_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    todos = get_todos(user_id, chat_id)

    if todos:
        todos_list = "Your To-Do list:\n"
        for todo_id, task, done in todos:
            status = "✅" if done else "⭕"
            todos_list += f"{status} {todo_id}: {task}\n"
        await update.message.reply_text(todos_list)
    else:
        await update.message.reply_text("Your To-Do list is empty.")

async def donetodo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /donetodo [todo_id]")
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    todo_id = int(context.args[0])

    if mark_todo_done(user_id, chat_id, todo_id):
        await update.message.reply_text(f"Todo {todo_id} marked as done.")
    else:
        await update.message.reply_text(f"Todo {todo_id} not found or already done.")

async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /remind [minutes] [text]")
        return
    
    delay_minutes = int(context.args[0])
    reminder_text = " ".join(context.args[1:])
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    await update.message.reply_text(f"I will remind you in {delay_minutes} minutes: {reminder_text}")

    # Schedule the reminder
    await asyncio.sleep(delay_minutes * 60)
    await context.bot.send_message(chat_id=chat_id, text=f"Reminder for {update.effective_user.mention_html()}: {reminder_text}", parse_mode="HTML")

async def bookmark_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /bookmark [url] [name]")
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    url = context.args[0]
    name = " ".join(context.args[1:])

    if add_bookmark(user_id, chat_id, url, name):
        await update.message.reply_text(f"Bookmark ‘{name}’ saved for {url}.")
    else:
        await update.message.reply_text(f"Bookmark ‘{name}’ already exists. Choose a different name.")

async def bookmarks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    bookmarks = get_bookmarks(user_id, chat_id)

    if bookmarks:
        bookmarks_list = "Your bookmarks:\n"
        for name, url in bookmarks:
            bookmarks_list += f"- [{name}]({url})\n"
        await update.message.reply_text(bookmarks_list, parse_mode="Markdown")
    else:
        await update.message.reply_text("You have no bookmarks.")

# --- Tools Commands ---
async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /calc [expression]")
        return
    
    expression = " ".join(context.args)
    try:
        # Using eval is dangerous, but for a simple calculator with trusted input, it might be acceptable.
        # For a production bot, a safer math expression parser should be used.
        result = eval(expression)
        await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        await update.message.reply_text(f"Error in calculation: {e}")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /weather [city]")
        return
    
    city = " ".join(context.args)
    url = f"https://wttr.in/{city}?format=3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                weather_data = await response.text()
                await update.message.reply_text(f"Weather in {city.title()}:\n{weather_data}")
            else:
                await update.message.reply_text(f"Could not fetch weather for {city}. Please check the city name.")

async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /qr [text_to_encode]")
        return
    
    text_to_encode = " ".join(context.args)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_to_encode)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    await update.message.reply_photo(photo=buffer, caption="Here is your QR code!")

async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Unit conversion feature not yet implemented.")

async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /currency [amount] [from_currency] [to_currency]")
        return
    
    try:
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()
    except ValueError:
        await update.message.reply_text("Invalid amount. Please provide a number.")
        return

    # Using exchangerate.host API (free for up to 1500 requests/month)
    url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols={to_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200 and data["success"]:
                if to_currency in data["rates"]:
                    rate = data["rates"][to_currency]
                    converted_amount = amount * rate
                    await update.message.reply_text(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
                else:
                    await update.message.reply_text(f"Could not find exchange rate for {to_currency}.")
            else:
                err_msg = data.get('error', 'Unknown error')
                await update.message.reply_text(f"Could not fetch exchange rates. Error: {err_msg}")

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /time [timezone] (e.g., Asia/Kolkata or UTC)")
        return
    
    timezone_str = " ".join(context.args)
    try:
        # This requires a more robust timezone library like pytz or zoneinfo
        # For simplicity, we'll just show UTC time for now if a specific timezone isn't easily parsed
        now_utc = datetime.datetime.utcnow()
        time_str = now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
        await update.message.reply_text(f"Current UTC time: {time_str}")
        await update.message.reply_text("Note: Advanced timezone support requires additional libraries.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}. Please provide a valid timezone.")

async def countdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /countdown [YYYY-MM-DD] [optional_event_name]")
        return
    
    try:
        target_date_str = context.args[0]
        target_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d")
        event_name = " ".join(context.args[1:]) if len(context.args) > 1 else "event"

        now = datetime.datetime.now()
        time_left = target_date - now

        if time_left.total_seconds() < 0:
            await update.message.reply_text(f"The {event_name} was {abs(time_left.days)} days ago.")
        else:
            days = time_left.days
            hours = time_left.seconds // 3600
            minutes = (time_left.seconds % 3600) // 60
            seconds = time_left.seconds % 60
            await update.message.reply_text(f"Countdown to {event_name}: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds left.")
    except ValueError:
        await update.message.reply_text("Invalid date format. Please use YYYY-MM-DD.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def wordcount_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /wordcount [text]")
        return
    
    text = " ".join(context.args)
    words = text.split()
    await update.message.reply_text(f"Word count: {len(words)}")

async def base64_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2 or context.args[0] not in ["encode", "decode"]:
        await update.message.reply_text("Usage: /base64 [encode/decode] [text]")
        return
    
    action = context.args[0]
    text = " ".join(context.args[1:])

    try:
        if action == "encode":
            encoded_bytes = base64.b64encode(text.encode("utf-8"))
            encoded_str = encoded_bytes.decode('utf-8')
            await update.message.reply_text(f"Encoded: {encoded_str}")
        else: # decode
            decoded_bytes = base64.b64decode(text.encode("utf-8"))
            decoded_str = decoded_bytes.decode('utf-8')
            await update.message.reply_text(f"Decoded: {decoded_str}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}. Make sure the text is valid for decoding.")

async def hash_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /hash [algorithm] [text] (e.g., sha256, md5)")
        return
    
    algorithm = context.args[0].lower()
    text = " ".join(context.args[1:])

    try:
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode("utf-8"))
        await update.message.reply_text(f"{algorithm.upper()} Hash: {hasher.hexdigest()}")
    except ValueError:
        await update.message.reply_text(f"Invalid hashing algorithm: {algorithm}. Supported: {hashlib.algorithms_available}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def shorten_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /shorten [url]")
        return
    
    url = context.args[0]
    await update.message.reply_text(f"Shortened URL (not actually shortened, just echoing): {url}")

async def password_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    length = 12 # Default length
    if context.args and context.args[0].isdigit():
        length = int(context.args[0])
        if length < 4 or length > 64:
            await update.message.reply_text("Password length must be between 4 and 64 characters.")
            return
    
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    password = "".join(random.choice(chars) for i in range(length))
    await update.message.reply_text(f"Generated Password: `{password}`", parse_mode="Markdown")

async def color_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Color info feature not yet implemented.")

async def emoji_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Emoji search feature not yet implemented.")

async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /reverse [text]")
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"Reversed text: {text[::-1]}")

async def upper_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /upper [text]")
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"Uppercase text: {text.upper()}")

async def lower_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /lower [text]")
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"Lowercase text: {text.lower()}")

# --- Fun Commands ---
async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a famous inspirational quote."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Tell a short, family-friendly joke."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide an interesting and little-known fact."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def flip_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(random.choice(["Heads", "Tails"]))

async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sides = 6
    if context.args and context.args[0].isdigit():
        sides = int(context.args[0])
        if sides < 1:
            await update.message.reply_text("Number of sides must be at least 1.")
            return
    await update.message.reply_text(f"Rolled a {random.randint(1, sides)}")

async def choose_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /choose [option1] | [option2] | ...")
        return
    
    options = " ".join(context.args).split("|")
    options = [opt.strip() for opt in options if opt.strip()]
    if len(options) < 2:
        await update.message.reply_text("Please provide at least two options separated by '|'.")
        return
    await update.message.reply_text(f"I choose: {random.choice(options)}")

async def rng_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2 or not context.args[0].isdigit() or not context.args[1].isdigit():
        await update.message.reply_text("Usage: /rng [min] [max]")
        return
    
    min_val = int(context.args[0])
    max_val = int(context.args[1])

    if min_val > max_val:
        await update.message.reply_text("Min value cannot be greater than max value.")
        return
    
    await update.message.reply_text(f"Random number: {random.randint(min_val, max_val)}")

async def eightball_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /8ball [question]")
        return
    
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
        "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
        "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don\'t count on it.", "My reply is no.", "My sources say no.",
        "Outlook not so good.", "Very doubtful."
    ]
    await update.message.reply_text(f"Magic 8-Ball says: {random.choice(responses)}")

async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a fun and harmless dare for a Telegram group chat."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide an interesting and thought-provoking truth question for a Telegram group chat."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def would_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = "Provide a 'Would you rather' question for a Telegram group chat."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /rate [thing_to_rate]")
        return
    
    thing = " ".join(context.args)
    rating = random.randint(1, 10)
    await update.message.reply_text(f"I rate '{thing}' a {rating}/10.")

async def ship_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /ship [name1] [name2]")
        return
    
    name1 = context.args[0]
    name2 = context.args[1]
    compatibility = random.randint(0, 100)
    await update.message.reply_text(f"{name1} and {name2} have a {compatibility}% compatibility!")

async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /roast [name]")
        return
    
    name = " ".join(context.args)
    prompt = f"Provide a lighthearted and funny roast for {name}. Keep it clean and not offensive."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def compliment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /compliment [name]")
        return
    
    name = " ".join(context.args)
    prompt = f"Provide a genuine and kind compliment for {name}."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

# --- Profile Commands ---
async def me_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    profile = get_user_profile(user.id)
    if profile:
        bio, afk_status, afk_reason, xp, level = profile
        status = f"AFK: {afk_reason}" if afk_status else "Online"
        await update.message.reply_text(
            f"**Your Profile:**\n"
            f"ID: `{user.id}`\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username}\n"
            f"Bio: {bio if bio else 'Not set'}\n"
            f"Status: {status}\n"
            f"Level: {level} (XP: {xp})",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Your profile is not set up yet. Use /setbio to add a bio.")

async def afk_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    reason = " ".join(context.args) if context.args else "away"
    set_afk_status(user_id, True, reason)
    await update.message.reply_text(f"{update.effective_user.first_name} is now AFK: {reason}")

async def bio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        user_id = update.effective_user.id
        profile = get_user_profile(user_id)
        if profile and profile[0]:
            await update.message.reply_text(f"Your current bio: {profile[0]}")
        else:
            await update.message.reply_text("You don't have a bio set. Use /setbio to add one.")
        return
    
    # If a user is mentioned, try to get their bio
    # This part requires more advanced entity parsing from Telegram messages
    await update.message.reply_text("To view another user's bio, please mention them (feature not fully implemented yet).")

async def setbio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /setbio [your_bio_text]")
        return
    
    user_id = update.effective_user.id
    bio_text = " ".join(context.args)
    create_or_update_user_profile(user_id, bio=bio_text)
    await update.message.reply_text("Your bio has been updated.")

async def level_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    profile = get_user_profile(user_id)
    if profile:
        xp = profile[3]
        level = profile[4]
        await update.message.reply_text(f"You are Level {level} with {xp} XP.")
    else:
        await update.message.reply_text("Your profile is not set up yet. Send some messages to gain XP!")

# --- Group Commands ---
async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or "|" not in " ".join(context.args):
        await update.message.reply_text("Usage: /poll [question] | [option1] | [option2] | ...")
        return
    
    parts = " ".join(context.args).split("|")
    question = parts[0].strip()
    options = [opt.strip() for opt in parts[1:] if opt.strip()]

    if not question or len(options) < 2 or len(options) > 10:
        await update.message.reply_text("Please provide a question and 2-10 options for the poll.")
        return
    
    await update.effective_chat.send_poll(
        question=question,
        options=options,
        is_anonymous=False, # For group stats, usually not anonymous
        allows_multiple_answers=False,
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # This would require more complex aggregation from the messages table
    await update.message.reply_text("Group statistics feature not yet implemented in detail.")

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    rules = get_rules(chat_id)
    if rules:
        await update.message.reply_text(f"**Group Rules:**\n{rules}", parse_mode="Markdown")
    else:
        await update.message.reply_text("No rules have been set for this group. Admins can use /setrules.")

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    response_msg = f"**Your ID:** `{user.id}`\n"
    if user.username:
        response_msg += f"**Your Username:** @{user.username}\n"
    response_msg += f"**Chat ID:** `{chat.id}`\n"
    if chat.title:
        response_msg += f"**Chat Name:** {chat.title}\n"
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        response_msg += f"**Replied User ID:** `{replied_user.id}`\n"
        if replied_user.username:
            response_msg += f"**Replied Username:** @{replied_user.username}\n"
    
    await update.message.reply_text(response_msg, parse_mode="Markdown")

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to report it.")
        return
    
    # This would typically forward the message to admins or a log channel
    await update.message.reply_text("Message reported to admins (feature not fully implemented).")

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /feedback [your_feedback]")
        return
    
    feedback_text = " ".join(context.args)
    # This would typically send feedback to a specific channel or developer
    await update.message.reply_text("Thank you for your feedback! (feature not fully implemented).")

async def groupinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("This command only works in groups.")
        return
    
    info_msg = f"**Group Info:**\n"
    info_msg += f"Title: {chat.title}\n"
    info_msg += f"ID: `{chat.id}`\n"
    info_msg += f"Type: {chat.type}\n"
    if chat.description:
        info_msg += f"Description: {chat.description}\n"
    
    await update.message.reply_text(info_msg, parse_mode="Markdown")

# --- Admin Commands ---
async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if update.effective_chat.type == "private":
        await update.message.reply_text("Admin commands only work in groups.")
        return False
    
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ["creator", "administrator"]:
        return True
    else:
        await update.message.reply_text("You must be an admin to use this command.")
        return False

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    
    admin_help_text = """
**Admin Commands:**
/mute [user] [duration] - Mute a user
/unmute [user] - Unmute a user
/warn [user] [reason] - Warn a user
/unwarn [user] - Remove last warn from a user
/warns [user] - Show warns for a user
/pin - Pin replied message
/unpin - Unpin message
/announce [text] - Send an announcement
/tagall - Mention all group members (use with caution)
/setrules [text] - Set group rules
/addcmd [cmd] [response] - Add custom command
/delcmd [cmd] - Delete custom command
/slowmode [seconds] - Set slow mode
/purge [count] - Delete recent messages
"""
    await update.message.reply_text(admin_help_text, parse_mode="Markdown")

async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to mute them.")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    
    # Mute for 1 hour by default, or specified duration
    until_date = datetime.datetime.now() + datetime.timedelta(hours=1)
    if len(context.args) > 0 and context.args[0].isdigit():
        duration_hours = int(context.args[0])
        until_date = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)

    try:
        await context.bot.restrict_chat_member(
            chat_id,
            target_user.id,
            permissions=telegram.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await update.message.reply_text(f"User {target_user.full_name} has been muted.")
    except Exception as e:
        await update.message.reply_text(f"Could not mute user: {e}")

async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to unmute them.")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.restrict_chat_member(
            chat_id,
            target_user.id,
            permissions=telegram.ChatPermissions(can_send_messages=True, can_send_audios=True, can_send_documents=True, can_send_photos=True, can_send_videos=True, can_send_video_notes=True, can_send_voice_notes=True, can_send_polls=True, can_send_other_messages=True, can_add_web_page_previews=True, can_change_info=False, can_invite_users=True, can_pin_messages=False, can_manage_topics=False)
        )
        await update.message.reply_text(f"User {target_user.full_name} has been unmuted.")
    except Exception as e:
        await update.message.reply_text(f"Could not unmute user: {e}")

async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to warn them.")
        return
    
    target_user = update.message.reply_to_message.from_user
    admin_user = update.effective_user
    chat_id = update.effective_chat.id
    reason = " ".join(context.args) if context.args else "No reason provided."

    add_warning(target_user.id, chat_id, admin_user.id, reason)
    await update.message.reply_text(f"User {target_user.full_name} warned for: {reason}")

async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to unwarn them.")
        return
    
    target_user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    if remove_last_warning(target_user.id, chat_id):
        await update.message.reply_text(f"Last warning for {target_user.full_name} removed.")
    else:
        await update.message.reply_text(f"No warnings found for {target_user.full_name}.")

async def warns_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    
    target_user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    chat_id = update.effective_chat.id

    warnings = get_warnings(target_user.id, chat_id)
    if warnings:
        warn_list = f"Warnings for {target_user.full_name}:\n"
        for i, (reason, admin_id, timestamp) in enumerate(warnings):
            warn_list += f"{i+1}. Reason: {reason} (Admin: {admin_id}, Time: {timestamp})\n"
        await update.message.reply_text(warn_list)
    else:
        await update.message.reply_text(f"No warnings for {target_user.full_name}.")

async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to pin it.")
        return
    
    try:
        await context.bot.pin_chat_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.reply_to_message.message_id,
            disable_notification=False
        )
        await update.message.reply_text("Message pinned.")
    except Exception as e:
        await update.message.reply_text(f"Could not pin message: {e}")

async def unpin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    
    try:
        await context.bot.unpin_chat_message(
            chat_id=update.effective_chat.id,
            message_id=update.message.reply_to_message.message_id if update.message.reply_to_message else None
        )
        await update.message.reply_text("Message unpinned.")
    except Exception as e:
        await update.message.reply_text(f"Could not unpin message: {e}")

async def announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not context.args:
        await update.message.reply_text("Usage: /announce [your_announcement]")
        return
    
    announcement_text = " ".join(context.args)
    await update.effective_chat.send_message(f"**Announcement:**\n{announcement_text}", parse_mode="Markdown")

async def tagall_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    
    # This is a highly disruptive command, use with extreme caution.
    # Telegram API does not provide a direct way to get all user IDs in a group.
    # This would typically involve iterating through chat members, which can be rate-limited or incomplete.
    await update.message.reply_text("Tagging all members is not directly supported by the Telegram Bot API in a reliable way for large groups. Use with extreme caution and consider alternatives.")

async def setrules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not context.args:
        await update.message.reply_text("Usage: /setrules [your_group_rules]")
        return
    
    chat_id = update.effective_chat.id
    rules_text = " ".join(context.args)
    set_rules(chat_id, rules_text)
    await update.message.reply_text("Group rules have been set.")

async def addcmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addcmd [command_name] [response_text]")
        return
    
    chat_id = update.effective_chat.id
    command_name = context.args[0].lower()
    response_text = " ".join(context.args[1:])

    if not command_name.startswith("/"):
        command_name = "/" + command_name

    if add_custom_command(chat_id, command_name, response_text):
        await update.message.reply_text(f"Custom command ‘{command_name}’ added.")
    else:
        await update.message.reply_text(f"Custom command ‘{command_name}’ already exists.")

async def delcmd_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not context.args:
        await update.message.reply_text("Usage: /delcmd [command_name]")
        return
    
    chat_id = update.effective_chat.id
    command_name = context.args[0].lower()

    if not command_name.startswith("/"):
        command_name = "/" + command_name

    if delete_custom_command(chat_id, command_name):
        await update.message.reply_text(f"Custom command ‘{command_name}’ deleted.")
    else:
        await update.message.reply_text(f"Custom command ‘{command_name}’ not found.")

async def slowmode_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /slowmode [seconds] (0 to disable)")
        return
    
    chat_id = update.effective_chat.id
    seconds = int(context.args[0])

    try:
        await context.bot.set_chat_slow_mode(chat_id, seconds)
        if seconds > 0:
            await update.message.reply_text(f"Slow mode set to {seconds} seconds.")
        else:
            await update.message.reply_text("Slow mode disabled.")
    except Exception as e:
        await update.message.reply_text(f"Could not set slow mode: {e}")

async def purge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_admin(update, context):
        return
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /purge [number_of_messages]")
        return
    
    chat_id = update.effective_chat.id
    num_messages = int(context.args[0])

    if num_messages < 1 or num_messages > 100:
        await update.message.reply_text("You can purge between 1 and 100 messages at a time.")
        return
    
    # Get message IDs to delete. Telegram API requires individual message IDs.
    # This is a simplified approach, a more robust solution would involve fetching messages.
    message_ids_to_delete = []
    for i in range(num_messages):
        message_ids_to_delete.append(update.message.message_id - i) # Assuming consecutive messages
    
    try:
        await context.bot.delete_messages(chat_id, message_ids_to_delete)
        await update.message.reply_text(f"Purged {num_messages} messages.")
    except Exception as e:
        await update.message.reply_text(f"Could not purge messages. Error: {e}")

# --- Settings Commands ---
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    settings = get_chat_settings(chat_id)
    if settings:
        lang, notif_on = settings
        await update.message.reply_text(
            f"**Current Settings:**\n"
            f"Language: {lang}\n"
            f"Notifications: {'On' if notif_on else 'Off'}",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("No settings found. Default settings are applied.")

async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /setlang [language_code] (e.g., en, my)")
        return
    
    chat_id = update.effective_chat.id
    lang_code = context.args[0].lower()
    update_chat_settings(chat_id, language=lang_code)
    await update.message.reply_text(f"Language set to {lang_code}.")

async def setnotif_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or context.args[0].lower() not in ["on", "off"]:
        await update.message.reply_text("Usage: /setnotif [on/off]")
        return
    
    chat_id = update.effective_chat.id
    status = context.args[0].lower() == "on"
    update_chat_settings(chat_id, notifications_on=status)
    notif_status = 'on' if status else 'off'
    await update.message.reply_text(f"Notifications turned {notif_status}.")

# --- Book Search Command ---
async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /book [query]")
        return
    
    query = " ".join(context.args)
    url = f"http://openlibrary.org/search.json?q={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200 and data["docs"]:
                books = data["docs"][:5] # Get top 5 results
                book_list = "**Top 5 Book Results:**\n"
                for book in books:
                    title = book.get("title", "N/A")
                    author = ", ".join(book.get("author_name", ["N/A"]))
                    first_publish_year = book.get("first_publish_year", "N/A")
                    # Construct a potential download link (Open Library doesn't directly host all books)
                    # This is a placeholder, actual download links would require more logic or specific APIs
                    cover_key = book.get('cover_edition_key', '')
                    download_link = f"https://openlibrary.org/works/{cover_key}" if cover_key else "No direct download link available."
                    
                    book_list += f"\n**Title:** {title}\n"
                    book_list += f"**Author:** {author}\n"
                    book_list += f"**First Publish Year:** {first_publish_year}\n"
                    book_list += f"**More Info/Potential Download:** {download_link}\n"
                await update.message.reply_text(book_list, parse_mode="Markdown")
            else:
                await update.message.reply_text(f"No books found for ‘{query}’.")

