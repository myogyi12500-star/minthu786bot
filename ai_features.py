import os
from openai import OpenAI

# Initialize OpenAI client - uses OPENAI_API_KEY env var
# If deployed on your own server, set OPENAI_API_KEY to your Gemini API key
# and OPENAI_BASE_URL to https://generativelanguage.googleapis.com/v1beta/openai/
client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    api_key=os.environ.get("OPENAI_API_KEY", "your-gemini-api-key-here"),
)

async def generate_text_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

async def ask_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a question after /ask.")
        return
    prompt = " ".join(context.args)
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def search_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a query after /search.")
        return
    query = " ".join(context.args)
    prompt = f"Provide information about: {query}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def define_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a term to define after /define.")
        return
    term = " ".join(context.args)
    prompt = f"Define the term: {term}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def code_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a programming query after /code.")
        return
    code_query = " ".join(context.args)
    prompt = f"Generate code or explain programming concept for: {code_query}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def imagine_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a description for the image after /imagine.")
        return
    image_description = " ".join(context.args)
    await update.message.reply_text("Image generation is not directly supported by the current Gemini model. Please use a dedicated image generation tool.")

async def news_command(update, context):
    prompt = "Provide a summary of recent major news headlines."
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def explain_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic to explain after /explain.")
        return
    topic = " ".join(context.args)
    prompt = f"Explain: {topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def summarize_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide text to summarize after /summarize.")
        return
    text_to_summarize = " ".join(context.args)
    prompt = f"Summarize the following text: {text_to_summarize}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def grammar_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide text to check grammar for after /grammar.")
        return
    text_to_check = " ".join(context.args)
    prompt = f"Correct the grammar in the following text: {text_to_check}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def story_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a prompt for the story after /story.")
        return
    story_prompt = " ".join(context.args)
    prompt = f"Write a short story based on the following: {story_prompt}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def poem_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic for the poem after /poem.")
        return
    poem_topic = " ".join(context.args)
    prompt = f"Write a poem about: {poem_topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def lyrics_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic for the lyrics after /lyrics.")
        return
    lyrics_topic = " ".join(context.args)
    prompt = f"Write song lyrics about: {lyrics_topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def essay_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic for the essay after /essay.")
        return
    essay_topic = " ".join(context.args)
    prompt = f"Write a short essay on: {essay_topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def debate_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic for the debate after /debate.")
        return
    debate_topic = " ".join(context.args)
    prompt = f"Provide arguments for and against the following topic for a debate: {debate_topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def eli5_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a topic to explain like I\\'m 5 after /eli5.")
        return
    eli5_topic = " ".join(context.args)
    prompt = f"Explain the following like I\\'m 5: {eli5_topic}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def aiagent_command(update, context):
    if not context.args:
        await update.message.reply_text("Please provide a task for the AI agent after /aiagent.")
        return
    agent_task = " ".join(context.args)
    prompt = f"Act as an AI agent and respond to the following task: {agent_task}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def translate_command(update, context):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /translate [target_language] [text_to_translate]")
        return
    target_language = context.args[0]
    text_to_translate = " ".join(context.args[1:])
    prompt = f"Translate the following text to {target_language}: {text_to_translate}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)

async def detect_command(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /detect [text_to_detect_language]")
        return
    text_to_detect = " ".join(context.args)
    prompt = f"Detect the language of the following text: {text_to_detect}"
    response_text = await generate_text_response(prompt)
    await update.message.reply_text(response_text)
