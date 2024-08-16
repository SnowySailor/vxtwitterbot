import discord
from discord.ext import commands
from src.utils.logger import init_logger, log
from src.utils.utils import get_config
import urlextract
from urllib.parse import urlparse, parse_qs, urlencode
import time

def extract_and_parse_urls(text):
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(text)
    parsed_urls = [urlparse(url) for url in urls]
    return parsed_urls

def delete_query_params(url, params):
    query = parse_qs(url.query, keep_blank_values=True)
    for param in params:
        query.pop(param, None)
    return url._replace(query=urlencode(query, True))

def get_urls_with_fixed_domain_names(urls):
    ret = []
    for url in urls:
        if url.path == '':
            pass

        if url.netloc in ['www.x.com', 'www.twitter.com', 'x.com', 'twitter.com']:
            url = url._replace(netloc='vxtwitter.com')
            url = delete_query_params(url, ['t'])
            ret.append(url)
        elif url.netloc in ['www.instagram.com', 'instagram.com']:
            url = url._replace(netloc='ddinstagram.com')
            url = delete_query_params(url, ['igsh'])
            ret.append(url)
        elif url.netloc in ['pixiv.net', 'www.pixiv.net']:
            url = url._replace(netloc='phixiv.net')
            ret.append(url)
        elif url.netloc in ['reddit.com', 'www.reddit.com', 'old.reddit.com', 'www.old.reddit.com']:
            url = url._replace(netloc='rxddit.com')
            url = delete_query_params(url, ['utm_source', 'utm_medium', 'utm_name', 'utm_content', 'utm_term'])
            ret.append(url)
        elif url.netloc in ['www.tiktok.com', 'tiktok.com']:
            url = url._replace(netloc='tnktok.com')
            ret.append(url)
    return ret

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        log(f'Logged in as {bot.user} (ID: {bot.user.id})')
        log('------')

    async def on_message(self, message):
        urls = extract_and_parse_urls(message.content)
        urls = get_urls_with_fixed_domain_names(urls)
        if len(urls) > 0:
            replacement_message = '\n'.join([url.geturl() for url in urls])
            await message.channel.send(replacement_message)
            time.sleep(0.5)
            await message.edit(suppress=True)

init_logger()

intents = discord.Intents.default()
intents.members = True
intents.guild_messages = True
intents.message_content = True

bot = Bot(command_prefix=get_config('command_prefix', default = ';'), intents=intents)

def run_bot():
    bot.run(get_config('token'))
