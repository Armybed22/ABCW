import discord
import subprocess
from discord.ext import commands
import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_actionrow, create_button
from discord_slash.model import ButtonStyle
import asyncio
import sys
import re
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(
    name="profile",
    description="Показать профиль бота",
)
async def profile(ctx: SlashContext):
    invite_link = "https://discord.com/api/oauth2/authorize?client_id=1150385612839461036&permissions=8&scope=bot%20applications.commands"
    
    # Создаем кнопку "Ссылка на приглашение"
    button = create_button(
        style=ButtonStyle.URL,
        label="Ссылка на приглашение",
        url=invite_link
    )
    
    # Создаем строку с кнопкой
    action_row = create_actionrow(button)
    
    # Отправляем сообщение с кнопкой
    await ctx.send("Нажмите кнопку, чтобы пригласить бота на ваш сервер:", components=[action_row])



TOKEN = 'MTE1MDM4NTYxMjgzOTQ2MTAzNg.GAnmQA.iZFFJAQbKcB_5RS3O4_Yp3xhb6e6cUdEkQYApo'

SERVER_ID = '1132324413610672179'
CHANNEL_ID = '1135941436093763625'
ROLE_NAME = 'CMD-BASH'
AUTHORIZED_USERS = ['742692469006794773', '1005041789020938290']

if len(sys.argv) > 1 and sys.argv[1] == "-w":
    PYTHON_COMMAND = 'python'
else:
    PYTHON_COMMAND = 'python3'
def clean_code(text):
    text = text.strip('`')
    text = re.sub(r'\bpy\b', '', text)
    return text

@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} готов к работе')


@bot.command()
async def execute(ctx, *, full_command):
    if str(ctx.author.id) in AUTHORIZED_USERS:
        author_roles = [role.name for role in ctx.author.roles]
        if ROLE_NAME in author_roles:
            try:
                parts = full_command.split()
                sudo_password = parts[0]
                command = ' '.join(parts[1:])
                
                process = subprocess.Popen(
                    f'echo {sudo_password} | sudo -S {command}',
                    shell=True,
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE,
                    encoding='utf-8'
                )
                output, _ = process.communicate(timeout=30)  
                await ctx.send(f'Результат выполнения команды:\n```\n{output}\n```')
            except subprocess.CalledProcessError as e:
                error_result = f'Произошла ошибка при выполнении команды:\n```\n{e.output}\n```'
                await ctx.send(error_result)
            except asyncio.TimeoutError:
                await ctx.send("Прошло слишком много времени выполнения команды.")
            except Exception as e:
                await ctx.send(f'Произошла ошибка: {str(e)}')

@bot.command()
async def clear(ctx, limit: int):
    try:
        await ctx.channel.purge(limit=limit + 1)
    except ValueError:
        await ctx.send("Пожалуйста, укажите корректное количество сообщений для удаления.")

@bot.command()
async def aplfh(ctx, *, code: str):
    try:
        # Удаляем знаки ``` ```
        code = clean_code(code)

        with open('aplfh_code.af', 'w') as file:
            file.write(code)
        
        process = subprocess.Popen(
            f'{PYTHON_COMMAND} aplfh.py -s aplfh_code.af',
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            encoding='utf-8'
        )
        output, _ = process.communicate(timeout=30)
        
        os.remove('aplfh_code.af')

        await ctx.send(f'Результат выполнения aplfh кода:\n```\n{output}\n```')
    except Exception as e:
        await ctx.send(f'Произошла ошибка: {str(e)}')

bot.run(TOKEN)