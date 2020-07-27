import discord
from discord.ext import commands, tasks
import random
import os

client = commands.Bot(command_prefix = '.')

@client.event
async def on_connect():
    print('bot connected!')

@client.event
async def on_disconnect():
    print('bot disconnected')

@client.event
async def on_ready():
    print('bot is ready!')

@client.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await client.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

@client.event
async def on_member_join(member):
    print('{} has joined a server.'.format(member))

@client.event
async def on_member_remove(member):
    print('{} has left.'.format(member))

#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send('Plase pass in all required arguments.')

#@client.command()
#async def ping(ctx):
#    await ctx.send('Pong! {}ms'.format(round(client.latency * 1000)))

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = [ 'As I see it, yes.',
                  'Ask again later.',
                  'Better not tell you now.',
                  'Cannot predict now.',
                  'Concentrate and ask again.',
                  'Dont count on it.',
                  'It is certain.',
                  'It is decidedly so.',
                  'Most likely.',
                  'My reply is no.',
                  'My sources say no.',
                  'Outlook not so good.',
                  'Outlook good.',
                  'Reply hazy, try again.',
                  'Signs point to yes.',
                  'Very doubtful.',
                  'Without a doubt.',
                  'Yes.',
                  'Yes  definitely.',
                  'You may rely on it.',
                  'Ask Nikk']
    await ctx.send('Question: {}\nAnswer: {}'.format(question,
                                                     random.choice(responses)))
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

client.run('NzMyODYxNjMwODM2MTEzNDE4.Xw6wlA.OsXJ_yVcqzmN3g9FGusW17PK848')
