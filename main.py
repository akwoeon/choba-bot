import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# 📂 파일에서 저장된 횟수를 불러오는 함수
def load_count():
    if os.path.exists("count.txt"):
        with open("count.txt", "r", encoding="utf-8") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

# 💾 파일에 새로운 횟수를 저장하는 함수
def save_count(count):
    with open("count.txt", "w", encoding="utf-8") as f:
        f.write(str(count))

# 봇이 켜질 때 기존 숫자를 가져옵니다
babo_count = load_count()

@bot.event
async def on_message(message):
    global babo_count
    
    if message.author == bot.user:
        return

    # 1. 채팅창에 '초바바보'라고 쳤을 때
    if message.content == '초바바보':
        babo_count += 1        # 횟수 1 증가
        save_count(babo_count) # 파일에 저장
        await message.channel.send(f'초바바보다!😀 지금까지 {babo_count}번 맞는말했다!')

    # 2. 채팅창에 '죽초바김초바'라고 쳤을 때
    elif message.content == '죽초바김초바':
        await message.channel.send('죽는다! 😀')

    # 3. 채팅창에 '/초기화'라고 쳤을 때 (새로 추가됨!)
    elif message.content == '/놀림초기화':
        babo_count = 0        # 횟수를 0으로 리셋
        save_count(babo_count) # 파일도 0으로 덮어쓰기
        await message.channel.send('🧹 놀림 횟수가 0번으로 초기화되었습니다!')

    await bot.process_commands(message)

# ⚠️ 맨 마지막 줄 작은따옴표 안에 유저님의 봇 토큰을 넣어주세요!
bot.run(''.strip())
