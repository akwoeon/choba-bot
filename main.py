import discord
from discord.ext import commands
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 🛡️ 가짜 웹 서버 설정 (UptimeRobot 접속용)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    # 렌더가 지정한 포트를 찾아서 연결 (기본값 10000)
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

# 웹 서버를 봇과 동시에 실행
threading.Thread(target=run_web_server, daemon=True).start()

# --- 여기서부터 디스코드 봇 코드 ---
intents = discord.Intents.default()
intents.message_content = True 

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

@bot.event
async def on_message(message):
    global babo_count
    if message.author == bot.user:
        return

    if message.content == '초바바보':
        babo_count += 1
        save_count(babo_count)
        await message.channel.send(f'초바바보 아니다! 지금까지 {babo_count}번 놀렸다!')

    elif message.content == '죽초바김초바':
        await message.channel.send('안죽는다! 😡')

    await bot.process_commands(message)

@bot.tree.command(name="초기화", description="초바바보 놀림 횟수를 0번으로 초기화합니다.")
async def reset_count(interaction: discord.Interaction):
    global babo_count
    babo_count = 0         
    save_count(babo_count) 
    await interaction.response.send_message('🧹 놀림 횟수가 0번으로 초기화되었습니다!')

# 환경 변수에서 토큰 가져와서 실행
bot.run(os.environ.get('DISCORD_TOKEN').strip())
