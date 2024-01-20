import discord, asyncio, os, requests
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = commands.Bot(command_prefix='!', self_bot=True)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name='Hello World'), status=discord.Status.dnd)

@bot.event
async def on_message(message):

    if message.author == bot.user: # keep it like this until you know what you're doing (or you'll have a bad time)
        if message.content.startswith('!chat'):
            message_text = message.clean_content.replace('!chat', '').strip()
            message_reply = get_response(message_text)

            if isinstance(message.channel, discord.DMChannel):
                async with message.channel.typing():
                    await asyncio.sleep(10)
                    await message.channel.send(message_reply)
            else:
                async with message.channel.typing():
                    await asyncio.sleep(10)
                    await message.reply(message_reply)

# if not working, try to change the authorization token/model or switch to a different platform
def get_response(message):

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer mcr-0QVlNBfRo0xUc9239k',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': message,
        'max_new_tokens': 100,
        'min_tokens': 10,
        'stopping_strings': [],
        'ban_eos_token': False,
        'temperature': 1,
        'repetition_penalty': 1.1,
        'presence_penalty': 0,
        'frequency_penalty': 0,
        'top_k': 65,
        'top_p': 0.5,
        'top_a': 0,
        'timeout': None,
        'allow_logging': None
    }

    response = requests.post('https://neuro.mancer.tech/webui/mytholite/api/v1/generate', headers=headers, json=data)

    if response.status_code == 200:
        output = response.json()
        results = output['results']

        if results:
            text = results[0]['text']
            return text
        else:
            return response.text
    else:
        return response.text

bot.run(TOKEN)