import discord
import asyncio
import random

from .abc import MixinMeta
from .menus import menus

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import pagify

# Huge thankyou to Jojo for writing this cog on his personal repo.

class Mjolnir(MixinMeta):
    """Attempt to lift Thor's hammer!"""
    __version__ = "0.1.1"

    async def red_delete_data_for_user(self, *, requester, user_id):
        await self.config.user_from_id(user_id).clear()

    @commands.command()
    async def lifted(self, ctx):
        lifted = await self.config.user(ctx.author).lifted()
        if lifted == 1:
            sending = f"You have lifted Mjolnir 1 time."
        else:
            sending = f"You have lifted Mjolnir {lifted} times."
        await ctx.send(content=sending)

    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.command()
    async def trylift(self, ctx):
        lifted = random.randint(0, 100)
        if lifted >= 95:
            content = "The sky opens up and a bolt of lightning strikes the ground\nYou are worthy. Hail, son of Odin"
            lift = await self.config.user(ctx.author).lifted()
            lift += 1
            await self.config.user(ctx.author).lifted.set(lift)
        else:
            content = random.choice((
                "The hammer is strong, but so are you. Keep at it", "Mjolnir budges a bit but remains steadfast, as you should.",
                "You've got this!"))
        await ctx.send(content=content)

    @commands.command()
    async def liftedboard(self, ctx):
        all_users = await self.config.all_users()
        board = sorted(
            all_users.items(), key=lambda m: m[0]
        )
        sending = []
        for user in board:
            _user = await self.bot.get_or_fetch_user(user[0])
            name = _user.display_name
            amount = user[1]["lifted"]
            sending.append(f"**{name}:** {amount}")
        sending = list(pagify("\n".join(sending)))
        if not len(sending):
            embed = discord.Embed(
                title="Mjolnir!",
                description=f"No one has lifted Mjolnir yet!\nWill you be the first? Try `{ctx.clean_prefix}`",
                colour=discord.Colour.blue()
            )
            return await ctx.send(embed=embed)
        menu = menus.MjolnirMenu(source=menus.MjolnirPages(sending))
        await menu.start(ctx=ctx, channel=ctx.channel)

    async def cog_check(self, ctx: commands.Context):
        return ctx.guild is not None