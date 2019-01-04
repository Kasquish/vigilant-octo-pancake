import discord
from discord.ext import commands

@commands.command(pass_context = True)
async def crazyTestCommand(ctx,*args):
    await ctx.send("Pants!")
