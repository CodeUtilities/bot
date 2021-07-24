from replit import db
from discord.ext import commands
from flask import Flask, redirect
from threading import Thread
import discord
import os
import json
import urllib.request
import datetime

try:
  import localconstants as constants
except:
  import constants

prefix = "-"
client = commands.Bot(command_prefix=f"{prefix}", intents=discord.Intents.all())

global config_qa
config_qa = 1
if "config_qa" in db.keys():
  config_qa = db["config_qa"]

domain = "n8j5srrv39fz.runkit.sh"

app = Flask('')
@app.route('/')
def home():
    return redirect("https://l.lnk.repl.co/tfIl")
def run():
    app.run(host='0.0.0.0', port=8080)
t = Thread(target=run)
t.start()

@client.remove_command("help")
@client.command(no_pm=True, name="status")
async def status(ctx, * , msg="none"):
  await permsCalc(ctx)
  if msg == "none":
    await errorSend(ctx.channel, "Invalid argument at possition 0", "none")
    return()
  if len(msg) > 1000:
    await errorSend(ctx.channel, "The message must be 1000 chars or fewer.", "none")
    return()
  if permInt < 4:
    await errorSend(ctx.channel, "This command requires DEVELOPER permissions to use!", f"{perm}")
    return()
  await client.change_presence(activity=discord.Game(msg))
  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  #await setStatus(statusType, msg)
  embed.add_field(name="Succesful!", value=f"Sucsessfuly set status to: ```Playing {msg}```")
  await ctx.send(embed=embed)
  db["discordPresence"] = msg

async def setStatus(statusType, msg):
  if statusType == "playing":
    await client.change_presence(activity=discord.Game(msg))

@client.command(no_pm=True, name="say")
async def say(ctx,* , msg="none"):
  await permsCalc(ctx)
  if msg == "none":
    await errorSend(ctx.channel, "Invalid argument at possition 0", "none")
    return()
  if permInt < 2:
    await errorSend(ctx.channel, "This command requires CONTRIBUTOR permissions to use!", f"{perm}")
    return()
  if len(msg) > 1000:
    await errorSend(ctx.channel, "The message must be 1000 chars or fewer.", "none")
    return()
  await ctx.send(msg)
  await ctx.message.delete()

@client.command(no_pm=True, name="test")
async def test(ctx):
  guild = client.get_guild(660239763479068713)
  msg = guild.get_msg(822507216061464586)
  print(msg)
  
@client.command(no_pm=True, name="help")
async def help(ctx):
  if ctx.channel.id in constants.allowed_channels:
    await permsCalc(ctx)
    embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.add_field(name="Help Menu:", value="-help - Shows this menu.\n-faq - Most asked questions and answers.\n-status - Set the bots status.\n-player [player] - View a players profile.\n-autorespond - Toggles autoresponder.", inline=False)
    embed.set_footer(text=f"Permissions: {perm}")

    await ctx.send(embed=embed)

@client.command(no_pm=True, name="autorespond")
async def autorespond(ctx):
  await permsCalc(ctx)

  if permInt < 4:
    await errorSend(ctx.channel, "This command requires DEVELOPER permissions to use!", f"{perm}")
    return()
  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3)
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  global config_qa
  if config_qa == 1:
    config_qa = 0
    embed.add_field(name="Succesful!", value="Autoresponder has been disabled.")
  else:
    config_qa = 1
    embed.add_field(name="Succesful!", value="Autoresponder has been enabled.")
  db["config_qa"] = config_qa
  await ctx.send(embed=embed)

@client.command(no_pm=True, name="faq")
async def faq(ctx, tag="list"):
  await permsCalc(ctx)
  #if permInt < 3:
  #  await errorSend(ctx.channel, "This command requires CONTRIBUTOR permissions to use!", f"{perm}")
  #  return()
  tags = ["nbs","install","schem2df","itemapi","nbslength","optifine","darkmode"]
  tagDes = ["nbs -  View how to import and use nbs songs on DiamondFire.","install - View how to install CodeUtilities.","schem2df - View how to use Schem2DF on DiamondFire.","itemapi - View how to use codeutilities item api.","nbslength - View how to get a songs length in seconds.","optifine - View how to use optifine on fabric.","darkmode - View how to use menu darkmode."]
  if tag not in tags:
    embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    embed.add_field(name="F&Q List:", value="\n".join(tagDes))
    await ctx.send(embed=embed)
    return()
  if tag == "schem2df":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I use Schem2DF on DiamondFire?", f"https://{domain}?doc=Importing-Structure-Files-to-DiamondFire-(Schem2DF) ")
  if tag == "install":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I install CodeUtilities?", f"https://{domain}?doc=Installation")
  if tag == "nbs":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I use NBS Songs on DiamondFire?", f"https://{domain}?doc=Importing-Music-(NBS-Files)")
  if tag == "itemapi":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I use CodeUtilities Item API?", "https://raw.githubusercontent.com/CodeUtilities/bot/main/faq/itemapi")
  if tag == "nbslength":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I get a songs length in seconds?", "https://raw.githubusercontent.com/CodeUtilities/bot/main/faq/nbslength")
  if tag == "optifine":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I use optifine on fabric?", "https://raw.githubusercontent.com/CodeUtilities/bot/main/faq/optifine")
  if tag == "darkmode":
    await tagReply(ctx, ctx.channel, ctx.author, "How do I use menu darkmode?", "https://raw.githubusercontent.com/CodeUtilities/bot/main/faq/darkmode")

@client.command(no_pm=True, name="player")
async def player(ctx, player="a"):
  if player == "a":
    if ctx.author.nick == None:
      player = ctx.author.name
    else:
      player = ctx.author.nick
    
  await permsCalc(ctx)
  try:
    with urllib.request.urlopen(f"https://api.mojang.com/users/profiles/minecraft/{player}") as url:
      data = json.loads(url.read().decode())
      uuid = data["id"] 
    uuidFormat = [8,4,4,4,12]
    i = 0
    count = 0
    uuidFormatI = 0
    finaluuid = []
    while i != 32:
      count += 1
      finaluuid.append(uuid[i])
      if count == uuidFormat[uuidFormatI]:
        if count != 12:
          finaluuid.append("-")
        uuidFormatI += 1
        count = 0
      i += 1
    uuid = "".join(finaluuid)
  except:
    await errorSend(ctx.channel, "Player not found!", "none")
    return()
  try:
    with urllib.request.urlopen(f"https://codeutilities.github.io/data/cosmetics/players/{uuid}.json") as url:
      cosmetics = json.loads(url.read().decode())
    cape = cosmetics["cape"]
    hat = cosmetics["hat"]
    image = f"https://raw.githubusercontent.com/CodeUtilities/bot/main/capesHD/{cape}"
  except:
    cosmetics = "none"
    hat = "None"
    cape = "None"
    image = "https://raw.githubusercontent.com/CodeUtilities/bot/main/capesHD/None.png"
  try:
    cape = cape.replace("_", " ")
    cape = cape.replace(".png", "")
    cape = cape.title()
  except:
    cape = "None"
  try:
    hat = hat.replace("_", " ")
    hat = hat.replace(".json", "")
    hat = hat.title()
  except:
    hat = "None"
  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3, title=data["name"])
  embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  embed.add_field(name="UUID", value=uuid, inline=False)
  embed.add_field(name="Cape", value=cape, inline=False)
  embed.add_field(name="Hat", value=hat, inline=False)
  if image != "https://raw.githubusercontent.com/CodeUtilities/bot/main/capesHD/None.png":
    embed.set_thumbnail(url=image)
  await ctx.send(embed=embed)

@client.event
async def on_ready():
  print(f"Logged in as: {client.user}")
  if "discordPresence" in db.keys():
    await client.change_presence(activity=discord.Game(db["discordPresence"]))
  else:
    await client.change_presence(activity=discord.Game("DiamondFire!"))

async def errorSend(channel, error, showPerm):
  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xff0000)
  embed.add_field(name="Error!", value=error, inline=False)
  if showPerm != "none":
    embed.set_footer(text=f"Permissions: {showPerm}")
  await channel.send(embed=embed)

async def suggestionMsg(ctx, channel, type="suggestion"):
  #Suggestion Post
  if type != "suggestion":
    return
  member = ctx.author
  embed = discord.Embed(color=0xfff9b3)
  embed.add_field(name=f"📨 New {type} posted", value=f"{ctx.content}")
  embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
  embed.set_footer(text=f"Posted in #{ctx.channel}")
  channel = client.get_channel(channel)
  await channel.send(embed=embed)

@client.event
async def on_raw_message_delete(payload):
  if f"{payload.message_id}msg" in db.keys():
    ctx = db[f"{payload.message_id}msg"]
    
    author = ctx[0]
    authorID = ctx[1]
    content = ctx[2]
    url = ctx[3]
    channel = ctx[4]

    embed = discord.Embed(color=0xfff9b3)
    embed.add_field(name=f"📨 Message deleted!", value=f"{content}")
    embed.set_author(name=f"{author} ({authorID})", icon_url=f"{url}")
    embed.set_footer(text=f"In #{channel}")

    guild = client.get_guild(constants.guild_id)
    channel = guild.get_channel(constants.logs_channel)
    
    del db[f"{payload.message_id}msg"]
    await channel.send(embed=embed)


@client.event
async def on_message(ctx):
  db[f"{ctx.id}msg"] = [f"{ctx.author.name}", f"{ctx.author.id}", f"{ctx.content}", f"{ctx.author.avatar_url}", f"{ctx.channel}"]
  await client.process_commands(ctx)
  if ctx.channel.id == constants.suggestions_channel:
    await ctx.add_reaction(constants.upvote)
    await ctx.add_reaction(constants.downvote)
    await suggestionMsg(ctx, constants.discussion_channel, "suggestion")
    return()
  
  if ctx.channel.id == constants.crosspost_bot_messages_channel:
    if ctx.author.bot:
      await ctx.publish()

    return()

  if ctx.channel.id == constants.bug_reports_channel:
    await suggestionMsg(ctx, constants.bug_reports_channel_logs, "bug report")
    return()

  if ctx.channel.id == constants.beta_bug_reports_channel:
    await suggestionMsg(ctx, constants.beta_bug_reports_channel_logs, "beta bug report")
    return()

  if ctx.channel.id == constants.module_submissions_channel:
    if ctx.author.bot: return()
    guild = client.get_guild(constants.guild_id)
    channel = guild.get_channel(constants.module_approval_channel)
    member = ctx.author
    embed = discord.Embed(color=0x21ea83)
    embed.add_field(name="📨 New module posted", value=f"{ctx.content}\n{ctx.jump_url}")
    embed.set_author(name=f"{member.name}#{member.discriminator} <{member.id}>", icon_url=f"{member.avatar_url}")
    attachments = ""
    for attachment in ctx.attachments:
      attachments += f"**{attachment.filename}** {attachment.url}"
    if attachments != "":
      embed.add_field(name="📎 Attachments", value=attachments, inline=False)
    embed.set_footer(text=f"{ctx.id}")
    msg = await channel.send(embed=embed)
    await msg.add_reaction("✅")
    return()


  guild = client.get_guild(constants.guild_id)
  ignore = guild.get_role(constants.ignored_role)
  if ignore in ctx.author.roles:
    return()
  if config_qa == 1:
    chars = ["?","!"]
    msg = ctx.content.lower()
    for char in chars:
      msg = msg.replace(f"{char}", "")
    msg = msg.split()

    if "how" in msg:
      if "install" in msg:
        await tagReply(ctx, ctx.channel, ctx.author, "How do I install CodeUtilities?", f"https://{domain}?doc=Installation")
        await ctx.channel.send(f"{ctx.author.mention} please read the above info first! If you are still having issues please ask in <#661550032344055850>")
      
      if "schem2df" in msg:
        await tagReply(ctx, ctx.channel, ctx.author, "How do I use Schem2DF on DiamondFire?", f"https://{domain}?doc=Importing-Structure-Files-to-DiamondFire-(Schem2DF) ")
        await ctx.channel.send(f"{ctx.author.mention} please read the above info first! If you are still having issues please ask in <#661550032344055850>")      

      if "nbs" in msg:
        await tagReply(ctx, ctx.channel, ctx.author, "How do I use NBS Songs on DiamondFire?", f"https://{domain}?doc=Importing-Music-(NBS-Files)")
        await ctx.channel.send(f"{ctx.author.mention} please read the above info first! If you are still having issues please ask in <#661550032344055850>")

@client.event
async def on_reaction_add(reaction, user):
  if user.bot: return()
  if reaction.message.channel.id == constants.module_approval_channel:
    msgId = int(reaction.message.embeds[0].footer.text)
    channel = await client.fetch_channel(constants.module_submissions_channel)
    msg = await channel.fetch_message(msgId)
    
    embed = discord.Embed(color=0x21ea83)
    embed.add_field(name="📌 New module posted", value=f"{msg.content}")
    embed.set_author(name=f"{msg.author.name}", icon_url=f"{user.avatar_url}")
    attachments = ""
    for attachment in msg.attachments:
      attachments += f"**{attachment.filename}** {attachment.url}"
    if attachments != "":
      embed.add_field(name="📁 Files", value=attachments, inline=False)
    embed.set_footer(text=f"🔒 This module has been confirmed to be safe by a Contributor+ ({user.name}#{user.discriminator} <{user.id}>)\n📋 Submitter: {msg.author.name}#{msg.author.discriminator} <{msg.author.id}>")

    files_channel = await client.fetch_channel(constants.module_files_channel)
    msg = await files_channel.send(embed=embed)

async def tagReply(ctx, channel, user, question, url):
  file = urllib.request.urlopen(url)
  text = []
  text2 = []
  chars = 0
  for line in file:
    decoded_line = line.decode("utf-8")
    chars += len(decoded_line)
    if chars >= 1950:
      text2.append(decoded_line)
    else:
      text.append(decoded_line)

  if chars >= 1950:
    embed = discord.Embed(color=0xfff9b3, title=question, description=" ".join(text))
    await ctx.channel.send(embed=embed)
    embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3, description=" ".join(text2))
    await ctx.channel.send(embed=embed)
  else:
    embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3, title=question, description=" ".join(text))
    embed.set_author(name=user, icon_url=user.avatar_url)
    if url == "https://raw.githubusercontent.com/CodeUtilities/bot/main/faq/darkmode":
      await ctx.channel.send(embed=embed, content="https://youtu.be/_ebN_uLh4lU")
    else:
      await ctx.channel.send(embed=embed)

async def permsCalc(ctx):
  global perm
  global permInt

  if ctx.author.id in constants.bot_devs:
    permInt = 5
    perm = "BOT DEVELOPER"
    return()

  if ctx.author.id in constants.retired_devs:
    permInt = 4
    perm = "RETIRED DEVELOPER"
    return()

  for role in reversed(ctx.author.roles):
    role = role.id

    if role == constants.developer_role:
      permInt = 4
      perm = "DEVELOPER"
      return()

    if role == constants.contributor_role:
      permInt = 3
      perm = "CONTRIBUTOR"
      return()
    
    if role == constants.samman_role:
      permInt = 2
      perm = "SAMMAN"
      return()

    if role == constants.beta_tester_role:
      permInt = 1
      perm = "BETA TESTER"
      return()

  permInt = 0
  perm = "USER"


client.run(os.environ["DISCORD_TOKEN"])
