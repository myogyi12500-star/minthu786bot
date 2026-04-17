import sqlite3

DATABASE_NAME = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Messages table (already exists, ensure it's up-to-date)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Todos table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bookmarks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # User Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            bio TEXT,
            afk_status BOOLEAN DEFAULT FALSE,
            afk_reason TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            last_message_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Warnings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            admin_id INTEGER NOT NULL,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            chat_id INTEGER PRIMARY KEY,
            rules_text TEXT
        )
    """)

    # Custom Commands table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custom_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            command TEXT NOT NULL UNIQUE,
            response TEXT NOT NULL
        )
    """)

    # Settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            chat_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en',
            notifications_on BOOLEAN DEFAULT TRUE
        )
    """)

    conn.commit()
    conn.close()

def add_message(chat_id: int, message_id: int, text: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (chat_id, message_id, text) VALUES (?, ?, ?)",
        (chat_id, message_id, text)
    )
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, message_id, text FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_messages_by_chat(chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT message_id, text FROM messages WHERE chat_id = ?", (chat_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

# --- Notes Functions ---
def add_note(user_id: int, chat_id: int, name: str, content: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO notes (user_id, chat_id, name, content) VALUES (?, ?, ?, ?)",
                       (user_id, chat_id, name, content))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Note with this name already exists
    finally:
        conn.close()

def get_notes(user_id: int, chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, content FROM notes WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_note(user_id: int, chat_id: int, name: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE user_id = ? AND chat_id = ? AND name = ?", (user_id, chat_id, name))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# --- Todos Functions ---
def add_todo(user_id: int, chat_id: int, task: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (user_id, chat_id, task) VALUES (?, ?, ?)", (user_id, chat_id, task))
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    return todo_id

def get_todos(user_id: int, chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM todos WHERE user_id = ? AND chat_id = ? ORDER BY id", (user_id, chat_id))
    todos = cursor.fetchall()
    conn.close()
    return todos

def mark_todo_done(user_id: int, chat_id: int, todo_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET done = TRUE WHERE id = ? AND user_id = ? AND chat_id = ?", (todo_id, user_id, chat_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# --- Bookmarks Functions ---
def add_bookmark(user_id: int, chat_id: int, url: str, name: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bookmarks (user_id, chat_id, url, name) VALUES (?, ?, ?, ?)",
                       (user_id, chat_id, url, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Bookmark with this name already exists
    finally:
        conn.close()

def get_bookmarks(user_id: int, chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM bookmarks WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    bookmarks = cursor.fetchall()
    conn.close()
    return bookmarks

# --- User Profile Functions ---
def get_user_profile(user_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT bio, afk_status, afk_reason, xp, level FROM user_profiles WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def create_or_update_user_profile(user_id: int, bio: str = None, afk_status: bool = None, afk_reason: str = None, xp_change: int = 0):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user_profiles (user_id) VALUES (?)", (user_id,))

    updates = []
    params = []
    if bio is not None:
        updates.append("bio = ?")
        params.append(bio)
    if afk_status is not None:
        updates.append("afk_status = ?")
        params.append(afk_status)
    if afk_reason is not None:
        updates.append("afk_reason = ?")
        params.append(afk_reason)
    if xp_change != 0:
        updates.append("xp = xp + ?")
        params.append(xp_change)
        # Simple level up logic (can be more complex)
        cursor.execute("SELECT xp FROM user_profiles WHERE user_id = ?", (user_id,))
        current_xp = cursor.fetchone()[0] + xp_change
        new_level = int(current_xp / 100) + 1 # 100 XP per level
        updates.append("level = ?")
        params.append(new_level)

    if updates:
        params.append(user_id)
        cursor.execute(f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = ?", tuple(params))
    conn.commit()
    conn.close()

def set_afk_status(user_id: int, status: bool, reason: str = None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user_profiles (user_id) VALUES (?)", (user_id,))
    cursor.execute("UPDATE user_profiles SET afk_status = ?, afk_reason = ? WHERE user_id = ?", (status, reason, user_id))
    conn.commit()
    conn.close()

def get_afk_status(user_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT afk_status, afk_reason FROM user_profiles WHERE user_id = ?", (user_id,))
    status = cursor.fetchone()
    conn.close()
    return status

# --- Warnings Functions ---
def add_warning(user_id: int, chat_id: int, admin_id: int, reason: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO warnings (user_id, chat_id, admin_id, reason) VALUES (?, ?, ?, ?)",
                   (user_id, chat_id, admin_id, reason))
    conn.commit()
    conn.close()

def get_warnings(user_id: int, chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT reason, admin_id, timestamp FROM warnings WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    warnings = cursor.fetchall()
    conn.close()
    return warnings

def remove_last_warning(user_id: int, chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM warnings WHERE id = (SELECT MAX(id) FROM warnings WHERE user_id = ? AND chat_id = ?)",
                   (user_id, chat_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# --- Rules Functions ---
def set_rules(chat_id: int, rules_text: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO rules (chat_id, rules_text) VALUES (?, ?)", (chat_id, rules_text))
    conn.commit()
    conn.close()

def get_rules(chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT rules_text FROM rules WHERE chat_id = ?", (chat_id,))
    rules = cursor.fetchone()
    conn.close()
    return rules[0] if rules else None

# --- Custom Commands Functions ---
def add_custom_command(chat_id: int, command: str, response: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO custom_commands (chat_id, command, response) VALUES (?, ?, ?)",
                       (chat_id, command, response))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Command already exists
    finally:
        conn.close()

def get_custom_command(chat_id: int, command: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM custom_commands WHERE chat_id = ? AND command = ?", (chat_id, command))
    response = cursor.fetchone()
    conn.close()
    return response[0] if response else None

def delete_custom_command(chat_id: int, command: str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM custom_commands WHERE chat_id = ? AND command = ?", (chat_id, command))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

# --- Settings Functions ---
def get_chat_settings(chat_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO settings (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    cursor.execute("SELECT language, notifications_on FROM settings WHERE chat_id = ?", (chat_id,))
    settings = cursor.fetchone()
    conn.close()
    return settings

def update_chat_settings(chat_id: int, language: str = None, notifications_on: bool = None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO settings (chat_id) VALUES (?)", (chat_id,))

    updates = []
    params = []
    if language is not None:
        updates.append("language = ?")
        params.append(language)
    if notifications_on is not None:
        updates.append("notifications_on = ?")
        params.append(notifications_on)

    if updates:
        params.append(chat_id)
        cursor.execute(f"UPDATE settings SET {', '.join(updates)} WHERE chat_id = ?", tuple(params))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized and tables created/updated.")
