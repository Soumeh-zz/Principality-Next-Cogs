from cog import Cog, ConfigOption, SlashOption
from nextcord import Embed

class Help(Cog):

    class Config:
        information: ConfigOption('Write your bot\'s basic information here.', str)
        modules_per_page: ConfigOption(6, int, description="How many modules should be displayed per page?")

    async def ready(self):
        self.cog_pages = self.split_every(list(self.bot.cogs.keys()), self.config.modules_per_page)

    def split_every(self, list: list, count: int) -> int:
        return len([list[i::i+count] for i in range(0, len(list), count)])

    @Cog.slash_command(description="Bring up... idk, fuck", guild_ids=[802577295960571907])
    async def help(self, ctx):
        await ctx.response.send_message("Hello I am a slash command in a cog!")

    @help.subcommand()
    async def cog(self, ctx,
        cog: str = SlashOption(description="What Cog to get help for")
    ):
        pass

    @Cog.slash_command(description="List and explain Cogs", guild_ids=[802577295960571907])
    async def cogs(self, ctx, 
        page: int = SlashOption(description='What page of the modules to display', default=1)
    ):
        await ctx.response.send_message(embed=self.cogs_menu(page), ephemeral=False)
    
    def modules_menu(self, page: int = 1) -> Embed:
        # title
        embed = Embed(title=f"Cogs ({page}/{self.cog_pages})")

        # fields
        mpp = self.config['modules_per_page']
        for cog_name in self.bot.cogs.keys()[page*mpp::(page*mpp)+mpp]:
            cog = self.bot.cogs[cog_name]
            pass
            #embed.add_field(name=module.replace('_', ' ') + " Module", value=desc, inline=True)

        return embed