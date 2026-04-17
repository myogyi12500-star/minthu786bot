# Minthu786 Telegram Bot

Minthu786 is a comprehensive Telegram bot designed to provide a wide range of functionalities, from AI-powered commands to utility tools and group management features. It also includes a duplicate message detection system to maintain chat quality.

## Features

### Duplicate Message Detection
Automatically detects and warns about duplicate messages in a group, replying to the original message in Burmese.

### AI Commands (Powered by Gemini API)
- `/ask <query>`: Ask the AI a question.
- `/search <query>`: Get information on a topic.
- `/define <term>`: Get a definition for a term.
- `/code <query>`: Generate code or explain programming concepts.
- `/imagine <description>`: (Note: Image generation is not directly supported by the current Gemini model, this command will provide a textual response.)
- `/news`: Get a summary of recent major news headlines.
- `/explain <topic>`: Get an explanation of a topic.
- `/summarize <text>`: Summarize provided text.
- `/grammar <text>`: Check and correct grammar.
- `/story <prompt>`: Generate a short story.
- `/poem <topic>`: Write a poem.
- `/lyrics <topic>`: Write song lyrics.
- `/essay <topic>`: Write a short essay.
- `/debate <topic>`: Get arguments for and against a topic.
- `/eli5 <topic>`: Explain a topic like I'm 5.
- `/aiagent <task>`: Act as an AI agent for a given task.

### Translation
- `/translate`: (Not yet implemented)
- `/detect`: (Not yet implemented)

### Islamic
- `/dua`: (Not yet implemented)
- `/wisdom`: (Not yet implemented)
- `/quran`: (Not yet implemented)
- `/hadith`: (Not yet implemented)
- `/asmaulhusna`: (Not yet implemented)
- `/prayertime`: (Not yet implemented)

### Notes & Tasks
- `/note`: (Not yet implemented)
- `/notes`: (Not yet implemented)
- `/delnote`: (Not yet implemented)
- `/todo`: (Not yet implemented)
- `/todos`: (Not yet implemented)
- `/donetodo`: (Not yet implemented)
- `/remind`: (Not yet implemented)
- `/bookmark`: (Not yet implemented)
- `/bookmarks`: (Not yet implemented)

### Tools
- `/calc`: (Not yet implemented)
- `/weather`: (Not yet implemented)
- `/qr`: (Not yet implemented)
- `/convert`: (Not yet implemented)
- `/currency`: (Not yet implemented)
- `/time`: (Not yet implemented)
- `/countdown`: (Not yet implemented)
- `/wordcount`: (Not yet implemented)
- `/base64`: (Not yet implemented)
- `/hash`: (Not yet implemented)
- `/shorten`: (Not yet implemented)
- `/password`: (Not yet implemented)
- `/color`: (Not yet implemented)
- `/emoji`: (Not yet implemented)
- `/reverse`: (Not yet implemented)
- `/upper`: (Not yet implemented)
- `/lower`: (Not yet implemented)

### Fun
- `/quote`: (Not yet implemented)
- `/joke`: (Not yet implemented)
- `/fact`: (Not yet implemented)
- `/flip`: (Not yet implemented)
- `/roll`: (Not yet implemented)
- `/choose`: (Not yet implemented)
- `/rng`: (Not yet implemented)
- `/8ball`: (Not yet implemented)
- `/dare`: (Not yet implemented)
- `/truth`: (Not yet implemented)
- `/would`: (Not yet implemented)
- `/rate`: (Not yet implemented)
- `/ship`: (Not yet implemented)
- `/roast`: (Not yet implemented)
- `/compliment`: (Not yet implemented)

### Profile
- `/me`: (Not yet implemented)
- `/afk`: (Not yet implemented)
- `/bio`: (Not yet implemented)
- `/setbio`: (Not yet implemented)
- `/level`: (Not yet implemented)

### Group
- `/poll`: (Not yet implemented)
- `/stats`: (Not yet implemented)
- `/rules`: (Not yet implemented)
- `/id`: (Not yet implemented)
- `/report`: (Not yet implemented)
- `/feedback`: (Not yet implemented)
- `/groupinfo`: (Not yet implemented)

### Admin
- `/admin`: (Not yet implemented)
- `/mute`: (Not yet implemented)
- `/unmute`: (Not yet implemented)
- `/warn`: (Not yet implemented)
- `/unwarn`: (Not yet implemented)
- `/warns`: (Not yet implemented)
- `/pin`: (Not yet implemented)
- `/unpin`: (Not yet implemented)
- `/announce`: (Not yet implemented)
- `/tagall`: (Not yet implemented)
- `/setrules`: (Not yet implemented)
- `/addcmd`: (Not yet implemented)
- `/delcmd`: (Not yet implemented)
- `/slowmode`: (Not yet implemented)
- `/purge`: (Not yet implemented)

### Settings
- `/settings`: (Not yet implemented)
- `/setlang`: (Not yet implemented)
- `/setnotif`: (Not yet implemented)

### Book Search
- `/book`: (Not yet implemented)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/minthu786bot.git
    cd minthu786bot
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set environment variables:**
    -   `BOT_TOKEN`: Your Telegram bot token (provided in `main.py` for now, but recommended to use environment variables).
    -   `OPENAI_API_KEY`: Your API key for accessing the Gemini API via the OpenAI-compatible endpoint.

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## Deployment

Refer to `DEPLOY_GUIDE.md` for detailed deployment instructions on Railway.app, Render.com, and Oracle Cloud Free Tier.
