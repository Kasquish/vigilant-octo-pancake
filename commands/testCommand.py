import discord
from discord.ext import commands


class testCommandCog:
    

    def __init__(self, bot):
            self.bot = bot


    @commands.command(pass_context = True)
    async def crazyTestCommand(ctx,*args):
        await bot.say("Pants!")


def setup(bot):
    bot.add_cog(testCommandCog(bot))
