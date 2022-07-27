from principality.cog import ConfigOption, SlashOption
from principality.ext.game import GameCog

class Tic_Tac_Toe(GameCog):

    game_name = 'tictactoe'
    game_max_players = 2

    def __init__(self, *args, **kwargs):
        self.game_name = 'e'
        super().__init__(*args, **kwargs)

    #@Cog.slash_command()
    #async def test(self, ctx):
    #    await ctx.response.send_message(f"This value is {str(self.config['is_true'])}")

    #@Cog.listener()
    #async def on_member_join(self, member):
    #    print(member)