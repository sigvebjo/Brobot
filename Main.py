# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import time
import threading
import asyncio

import AnimHandler
import StorageHandler

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def handleAnim(currentFrame, interaction, animation):
    while (animation.hasNextFrame()):
        await asyncio.sleep(currentFrame.duration)
        currentFrame = animation.nextFrame()
        await interaction.edit_original_response(content=currentFrame.string)


@tree.command(name = "saveanimation", description = "Register a new animation. Format \"[string]^^[duration]|[string]^^duration|...\"\"a^^1|b^^0.5\"")
async def newAnimation(interaction, animname: str, animdata: str):
    animation = AnimHandler.stringToAnimation(animname, animdata)
    if StorageHandler.saveAnimation(animation):
        await interaction.response.send_message("Saved animation")
    else:
        await interaction.response.send_message("Animation with this name already exists")
    
@tree.command(name = "rawanimation", description = "Play an unsaved animation. Format \"[string]^^[duration]|[string]^^duration|...\"\"a^^1|b^^0.5\"")
async def rawAnimation(interaction, animdata: str):
    animation = AnimHandler.stringToAnimation("", animdata)
    
    currentFrame = animation.nextFrame()
    await interaction.response.send_message(currentFrame.string)
    await handleAnim(currentFrame, interaction, animation)
        
@tree.command(name = "playanimation", description = "Play an animation by name")
async def runAnimation(interaction, animname: str):
    animation = StorageHandler.getAnimation(animname)

    if animation == None:
        await interaction.response.send_message("No such animation: " + animname)
        return

    currentFrame = animation.nextFrame()
    await interaction.response.send_message(currentFrame.string)
    await handleAnim(currentFrame, interaction, animation)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    ###
    # Use this to syncronize the slash commands
    # Only usable by devs
    ###
    if message.content.startswith("/sync"):
        if message.author.id == 186179251203080193 or message.author.id == 275733181259448320:
            await tree.sync()
            message.channel.send("Syncronized commands!")
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)