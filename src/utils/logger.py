import logging
import discord
import sys

from discord.ext import commands
from src.utils.utils import get_config
from .utils import LoggerWriter

logger = None

def init_logger():
    global logger
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def logtofile(message: str, level: str = 'info'):
    getattr(logger, level)(message)

