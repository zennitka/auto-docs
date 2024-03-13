import discord
from discord.ext import commands, tasks
import gspread
import asyncio
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sacc1.json', scope)
client = gspread.authorize(creds)
sheet = client.open('docs name').sheet1
TOKEN = ' '
PREFIX = '/'
intents = discord.Intents().all()
roles_to_track = [role id]
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def update_sheet():
    guild = bot.get_guild(//id)
    if guild:
        members_with_roles = []
        user_ids = []
        roles = []
        for role_id in roles_to_track:
            role = discord.utils.get(guild.roles, id=role_id)
            if role:
                for member in guild.members:
                    if role in member.roles:
                        members_with_roles.append(member.display_name)
                        user_ids.append(str(member.id))
                        roles.append(role.name)
        if members_with_roles:
            data = []
            for i in range(len(members_with_roles)):
                row = [members_with_roles[i], user_ids[i], roles[i]]
                data.append(row)
            sheet.update('A2', data)

@tasks.loop(seconds=10)
async def automatic_update():
    await update_sheet()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    automatic_update.start()

# Создаем словарь для хранения информации о участниках
members_info = {}


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    for member in bot.get_all_members():
        await update_members_info(member)

@bot.command()
async def pm(ctx):
    guild = ctx.guild
    member = ctx.author
    channel_id = //channel id
    channel = bot.get_channel(channel_id)
    roles_to_assign = {
        //role id: "admin",
        //role id: "moder",
        //role id: "stazher"
    }
    role_to_assign = None
    for role_id, role_name in roles_to_assign.items():
        role = discord.utils.get(guild.roles, id=role_id)
        if role and role in member.roles:
            role_to_assign = role_name
            break
    if role_to_assign:
        member_info = members_info.get(str(member.id), {})  # Получаем информацию об участнике из словаря, если она есть
        member_info["name"] = member.display_name
        member_info["discord_id"] = str(member.id)
        member_info["position"] = role_to_assign
        member_info["steam_id"] = ""  # Временно оставляем пустым
        members_info[str(member.id)] = member_info
        save_members_info(roles_to_assign)
        load_members_info()  # Здесь загружаем информацию о участниках после ввода команды
        steam_id = members_info.get(str(member.id), {}).get("steam_id", "")
        if steam_id:
            if channel:
                await channel.send(f"+pm setgroup {steam_id} {role_to_assign}")
            await ctx.send("Сообщение успешно отправлено в указанный канал.")
        else:
            await ctx.send("Ваш Steam ID не найден. Пожалуйста, укажите его.")
    else:
        await ctx.send("У вас нет подходящих ролей для назначения.")


async def update_members_info(member):
    roles_to_assign = {
        //role id: "admin",
        //role id: "moder",
        //role id: "stazher"
    }
    for role_id, role_name in roles_to_assign.items():
        role = discord.utils.get(member.roles, id=role_id)
        if role:
            member_info = members_info.get(str(member.id), {})
            member_info["name"] = member.display_name
            member_info["discord_id"] = str(member.id)
            member_info["position"] = role_name
            member_info["steam_id"] = members_info.get(str(member.id), {}).get("steam_id", "")  # Используем текущий steam_id, если он есть
            members_info[str(member.id)] = member_info
            save_members_info(roles_to_assign)

def save_members_info(roles_to_assign):
    with open("members_info.txt", "w", encoding="utf-8") as file:
        for member_id, info in members_info.items():
            file.write(f"Discord ID: {info['discord_id']}\n")
            file.write(f"Name: {info['name']}\n")
            file.write(f"Position: {info['position']}\n")
            file.write(f"Steam ID: {info['steam_id']}\n")
            file.write("\n")

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await update_members_info(after)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    load_members_info()
    for member in bot.get_all_members():
        await update_members_info(member)

def load_members_info():
    with open("members_info.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        member_id = None
        info = {}
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    key, value = parts
                    if key == "Discord ID":
                        member_id = value
                    else:
                        info[key.lower()] = value
            else:
                if member_id:
                    members_info[member_id] = info
                    info = {}


bot.run(TOKEN)
