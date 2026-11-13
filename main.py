import discord
from discord import app_commands
from discord.ext import commands
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 🛡️ UptimeRobot 501 에러 방지용 웹 서버
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# 웹 서버 실행
threading.Thread(target=run_web_server, daemon=True).start()

# --- 디스코드 봇 코드 ---
intents = discord.Intents.default()
intents.message_content = True 

# 🔒 허용할 관리자 역할 ID
ADMIN_ROLE_ID = 1469520961337295080

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

def load_count():
    if os.path.exists("count.txt"):
        with open("count.txt", "r", encoding="utf-8") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_count(count):
    with open("count.txt", "w", encoding="utf-8") as f:
        f.write(str(count))

babo_count = load_count()

# 역할 확인용 도우미 함수
def has_admin_role(interaction: discord.Interaction) -> bool:
    if not interaction.guild or not isinstance(interaction.user, discord.Member):
        return False
    return any(role.id == ADMIN_ROLE_ID for role in interaction.user.roles)

@bot.event
async def on_message(message):
    global babo_count
    if message.author == bot.user:
        return

    # '초바바보' 또는 지정한 커스텀 이모지를 보냈을 때 작동
    if message.content in ['초바바보', '<:emoji_3:1561922713654788196>']:
        babo_count += 1
        save_count(babo_count)
        await message.channel.send(f'초바바보 아니다! 지금까지 {babo_count}번 놀렸다!')

    elif message.content == '죽초바김초바':
        await message.channel.send('안죽는다! 😡')

    await bot.process_commands(message)

# 🧹 초기화 명령어 (역할 제한)
@bot.tree.command(name="초기화", description="초바바보 놀림 횟수를 0번으로 초기화합니다.")
async def reset_count(interaction: discord.Interaction):
    if not has_admin_role(interaction):
        await interaction.response.send_message('🚫 이 명령어를 사용할 권한(역할)이 없습니다!', ephemeral=True)
        return

    global babo_count
    babo_count = 0         
    save_count(babo_count) 
    await interaction.response.send_message('🧹 놀림 횟수가 0번으로 초기화되었습니다!')

# 🔢 숫자 조절(설정) 명령어 (역할 제한)
@bot.tree.command(name="숫자설정", description="초바바보 놀림 횟수를 원하는 숫자로 변경합니다.")
@app_commands.describe(count="변경할 횟수 (0 이상의 숫자)")
async def set_count(interaction: discord.Interaction, count: int):
    if not has_admin_role(interaction):
        await interaction.response.send_message('🚫 이 명령어를 사용할 권한(역할)이 없습니다!', ephemeral=True)
        return

    if count < 0:
        await interaction.response.send_message('⚠️ 횟수는 0 이상의 숫자로만 설정할 수 있습니다.', ephemeral=True)
        return

    global babo_count
    babo_count = count
    save_count(babo_count)
    await interaction.response.send_message(f'✅ 놀림 횟수가 **{babo_count}번**으로 변경되었습니다!')

bot.run(os.environ.get('DISCORD_TOKEN').strip())
