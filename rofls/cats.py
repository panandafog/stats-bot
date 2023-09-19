import discord
import requests
import io

cats_url = 'https://cataas.com/cat'
filename = 'image.png'


def random_cat():
    bytes = requests.get(cats_url).content
    bytes_io = io.BytesIO(bytes)
    return discord.File(bytes_io, filename=filename)
