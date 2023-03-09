# This example requires the 'message_content' intent.

import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio

import AnimHandler
import StorageHandler

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

sentMessages = {}

def saveMessage(messageId, interaction, animation):
    sentMessages[messageId] = [interaction, animation]

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
    animation = AnimHandler.stringToAnimation(interaction.user.id, animname, animdata)
    if StorageHandler.saveAnimation(animation):
        await interaction.response.send_message("Saved animation")
    else:
        await interaction.response.send_message("Animation with this name already exists")
    
@tree.command(name = "rawanimation", description = "Play an unsaved animation. Format \"[string]^^[duration]|[string]^^duration|...\"\"a^^1|b^^0.5\"")
async def rawAnimation(interaction, animdata: str):
    animation = AnimHandler.stringToAnimation(interaction.user.id, "", animdata)
    
    currentFrame = animation.nextFrame()
    await interaction.response.send_message(currentFrame.string)
    await handleAnim(currentFrame, interaction, animation)
    saveMessage(interaction.id, interaction, animation)
        
@tree.command(name = "playanimation", description = "Play an animation by name")
async def runAnimation(interaction, animname: str):
    animation = StorageHandler.getAnimation(animname)

    if animation == None:
        await interaction.response.send_message("No such animation: " + animname)
        return

    currentFrame = animation.nextFrame()
    await interaction.response.send_message(currentFrame.string)
    await handleAnim(currentFrame, interaction, animation)
    saveMessage(interaction.id, interaction, animation)

@tree.command(name = "getanimationlist", description = "Get a list of all animations")
async def rawAnimation(interaction):
    await interaction.response.send_message("Here's a list of all stored animations:\n" + StorageHandler.getAllAnimationNamesAsString())

@tree.command(name = "deleteanimation", description = "Deletes an animation given a name. Must've been the creator.")
async def delAnimation(interaction, animname:str):
    animation = StorageHandler.getAnimation(animname)
    print(str(animation.author) + " : " + str(interaction.user.id))
    if interaction.user.id == animation.author and StorageHandler.deleteAnimation(animname):
        await interaction.response.send_message("Deleted the animation " + animname)
    else:
        await interaction.response.send_message("Either did not find the animation, or you are not its author.")

@client.event
async def on_reaction_add(reaction, _):
    if reaction.message.author.id == client.user.id:
        if reaction.message.interaction != None:
            if reaction.message.interaction.id in sentMessages:
                content = sentMessages[reaction.message.interaction.id]
                interaction = content[0]
                animation = content[1]
                animation.restart()
                currentFrame = animation.nextFrame()
                await interaction.edit_original_response(content=currentFrame.string)
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
            await message.channel.send("Syncronized commands!")

client.run(TOKEN)