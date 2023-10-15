import discord
import subprocess
from discord.ext import commands
import asyncio
import os
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'MTE1MDM4NTYxMjgzOTQ2MTAzNg.GVkLjw.VVgm_p5FiaAAw49lImMgsVrR_J0kMSuEYOuYZ8'

SERVER_ID = '1132324413610672179'
CHANNEL_ID = '1135941436093763625'
ROLE_NAME = 'CMD-BASH'
AUTHORIZED_USERS = ['742692469006794773', '1005041789020938290']
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
        code = code.strip('`')
        #autofagiya
        if (code.find(" os ")==-1) and (code.find("(os ") == -1) and (code.find(" os(") == -1) and (code.find("\nos(") == -1) and (code.find("\nos ") == -1) and (code[0] != "o" and code[1] != "s"):
            with open('aplfh_code.af', 'w') as file:
                file.write(code)
        
            process = subprocess.Popen(
                f'python3 new-aplfh/aplfh.py -s aplfh_code.af',
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
