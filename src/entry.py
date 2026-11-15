#!/usr/bin/env python3
"""
Gemma Discord Bot - Production version
Converts user queries to Ticket Tool documentation Q&A via Gemini
"""

import os
import sys
import logging
import discord
from discord.ext import commands
from google import genai
from google.genai import types as genai_types

# Example for FastAPI
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "live"}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get tokens/keys from environment
DISCORD_TOKEN = self.env.BOT_TOKEN
GOOGLE_API_KEY = self.env.GEMINI_API_KEY

# Validate required env vars
if not DISCORD_TOKEN:
    logger.error("DISCORD_TOKEN not found in environment variables")
    sys.exit(1)
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    sys.exit(1)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Gemini API client
client = genai.Client(api_key=GOOGLE_API_KEY)
model_id = "gemini-3.1-flash-lite"

# Privacy notice
PRIVACY_MESSAGE = (
    "\n\n---\n"
    "*Note: This is an AI generated response and may contain mistakes, please click <#571706435449257997> if you are not satisfied with this response. Your message was processed, do not share personal information. [Learn how this data was used.](<https://ai.google.dev/gemini-api/docs/logs-policy#use-data>)*"
)

# URL Variables
url1 = "https://docs.tickettool.xyz"
url2 = "https://tickettool.xyz/premium"
url3 = "https://discord.com/channels/509192800865353738/571706435449257997"

def get_gemini_response(user_content: str) -> str:
    """Generates responses from Gemini based on Ticket Tool documentation"""
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=user_content,
            generation_config={
                "thinking_summaries": "auto"
            },
            tools={
                {"type": "url_context"},
            },
            config=genai.types.GenerateContentConfig(
                system_instruction= f"You are an expert support assistant in working with Ticket Tool, a Discord bot. Your job is to answer user queries based on the official Ticket Tool documentation found at {url1} Ticket Tool premium plan costs and premium benefits are listed in  {url2}. Do not assume and hallucinate when thinking. If you can't find the answer to the question in the documentation, direct them to speak to human support in the [click here]{url3}."
            )
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


@bot.command()
async def ping(ctx):
    """Ping command to check bot latency"""
    await ctx.send(f'Pong! {round(bot.latency, 1)}ms')


@bot.event
async def on_ready():
    """Called when the bot successfully connects to Discord"""
    logger.info(f'Bot is online! Logged in as {bot.user}')


@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if bot was pinged or replied to
    is_pinged = bot.user in message.mentions
    is_replied_to = False

    # Check if message is a direct reply to the bot
    if message.reference and message.reference.resolved:
        if message.reference.resolved.author == bot.user:
            is_replied_to = True

    # Only respond if pinged or replied to
    if is_pinged or is_replied_to:
        # Clean the prompt (remove bot mention)
        clean_prompt = message.content.replace(f'<@{bot.user.id}>', '').strip()

        if not clean_prompt:
            await message.reply("Please provide a question or message!")
            return

        try:
            # Show typing indicator
            async with message.channel.typing():
                # Get AI response
                ai_reply = get_gemini_response(clean_prompt)
                final_response = f"{ai_reply}{PRIVACY_MESSAGE}"

                # Discord has a 2000 character limit; split if needed
                if len(final_response) > 2000:
                    # Split into chunks and send separately
                    chunks = [final_response[i:i+1990] for i in range(0, len(final_response), 1990)]
                    for i, chunk in enumerate(chunks):
                        if i == 0:
                            await message.reply(chunk)
                        else:
                            await message.channel.send(chunk)
                else:
                    await message.reply(final_response)

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await message.reply("Sorry, I encountered an error while processing your request. Please try again later.")


def main():
    """Main entry point"""
    try:
        logger.info("Starting Gemma bot...")
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
