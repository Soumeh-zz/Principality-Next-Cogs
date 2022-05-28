from nextcord import Embed
from principality.cog import  Cog, ConfigOption

class Counterpact_Status(Cog):

    class Config:
        lobby_ip: ConfigOption('', str, description="The IP to fetch lobby data from. Currently, the Counterpact lobby's information is private, so you will have to ask the developer for help. (Unless you are the developer, in which case, you probably know what to do)")
        lobby_port: ConfigOption(0, int, description="Refer to comment above.")

    async def ready(self):
        self.cpact_lobby = Counterpact_Lobby(self.config.lobby_ip, self.config.lobby_port)

    @Cog.slash_command(guild_ids=[418105205100642315, 964251827099033610, 971681845659959349])
    async def lobby(self, ctx):

        self.cpact_lobby.refresh()
        embed = Embed(
            title="Counterpact Lobby Status",
            color=0x6415ba,
            timestamp=self.cpact_lobby.last_check,
            url='http://discord.gg/gfKpVCv7Qd'
        )
        embed.set_footer(text="Last Updated")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/964252632023703582/977969364823318558/icon.png')

        if self.cpact_lobby.total_players == 1: embed.description = f"There is **{self.cpact_lobby.total_players}** player online."
        else: embed.description = f"There are **{self.cpact_lobby.total_players}** players online."
        if ctx.user.id == 685507245777354877: embed.description = embed.description.replace('online', 'among us')

        for server in self.cpact_lobby.servers:
            embed.add_field(
                name = server.name,
                value = f"""```hs
Players: {server.players}/{server.max_players}
Map: {server.map_name}```""",
                inline = False,
            )

        await ctx.response.send_message(embed=embed)

from datetime import datetime, timedelta
from json import loads
import socket

class Counterpact_Server():

    def __init__(self, json: dict):
        self.name = json['serverName']
        self.players = json['serverPlayers']
        self.max_players = json['serverMax']
        self.mods = json['serverMods']
        self.ip = json['serverIp']
        self.wsip = json['serverWSIp']
        self.port = json['serverPort']
        self.wsport = json['serverWSPort']
        self.map = json['serverMap']
        self.version = json['serverVersion']
        self.passkey = json['serverPasskey']

        self.full_ip = self.ip + ':' + str(self.port)
        self.map_name = self.map.rsplit('.', 1)[0]

class Counterpact_Lobby():

    def refresh(self):
        now = datetime.now()
        difference = (now - self.last_check).total_seconds()
        if difference < 30:
            return
        self._read_lobby()
        self._misc_data()
        self.last_check = datetime.now()

    def __init__(self, ip: str, port: int):
        self._tcp_ip = ip
        self._tcp_port = port

        self.last_check = datetime.now() - timedelta(seconds=30)
        self.refresh()

    def _read_lobby(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._tcp_ip, self._tcp_port))
        s.sendall(b"GET / HTTP/0.9\r\nLobby: True\r\n\r\n")
        data = s.recv(2048)
        s.close()
        json = loads(data.decode())
        self.servers = []
        for server_json in json:
            self.servers.append(Counterpact_Server(server_json))
    
    def _misc_data(self):
        self.total_players = sum([server.players for server in self.servers])
