from cog import Cog, ConfigOption, SlashOption

class Example(Cog):

    class Config:
        is_true: ConfigOption(True, bool, description="Whether or not this value is true")

    def load(self, bot):
        print('Loaded!')

    async def ready(self, bot):
        print('Async Loaded!')

    @Cog.slash_command(guild_ids=[802577295960571907])
    async def test(self, ctx):
        await ctx.respond(f"This value is {str(self.config['is_true'])} EEE")

    #@Cog.listener()
    #async def on_member_join(self, member):
    #    print('member')