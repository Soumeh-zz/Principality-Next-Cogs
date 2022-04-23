from cog import Cog, ConfigOption, SlashOption
from discord import Embed

class Help(Cog):

    class Config:
        information: ConfigOption('Write your bot\'s basic information here.', str)
        modules_per_page: ConfigOption(6, int, description="How many modules should be displayed per page?")

    async def ready(self, bot):
        self.bot = bot
        self.bot_mention = f'<@!{self.bot.user.id}>'

        self.modules = self.bot.cogs.keys()
        mpp = self.config['modules_per_page']
        self.module_pages = len([self.modules[i::i+mpp] for i in range(0, len(self.modules), mpp)])

    @Cog.slash_command(description="Bring up... idk, fuck", guild_ids=[802577295960571907])
    async def help(self, ctx):
        await ctx.response.send_message("Hello I am a slash command in a cog!")

    @Cog.slash_command(description="List and explain Modules", guild_ids=[802577295960571907])
    async def modules(self, ctx, 
        page: SlashOption(int, 'What page of the modules to display', default=1)
        ):
        await ctx.respond(embed=self.modules_menu(page), ephemeral=True)
    
    def modules_menu(self, page):
        # title
        embed = Embed(title=f"Modules ({page}/{self.module_pages})")

        # fields
        mpp = self.config['modules_per_page']
        for module in self.bot.cogs.keys()[page*mpp::(page*mpp)+mpp]:
            pass
            #embed.add_field(name=module.replace('_', ' ') + " Module", value=desc, inline=True)

        return embed