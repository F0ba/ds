import os
import asyncio
import disnake
from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен и ready!")

# ==========================================
# 1. OWNER (Управление структурой и бэкап)
# ==========================================

@bot.command()
@commands.has_role("Owner")
async def nuke_channel(ctx):
    """Пересоздает текущий канал (полная очистка с сохранением прав)"""
    pos = ctx.channel.position
    new_channel = await ctx.channel.clone(reason="Nuke channels")
    await ctx.channel.delete()
    await new_channel.edit(position=pos)
    await new_channel.send("💥 Канал был полностью пересоздан.")

@bot.command()
@commands.has_role("Owner")
async def lock(ctx):
    """Закрывает канал на чтение/отправку для @everyone"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Канал заблокирован.")

@bot.command()
@commands.has_role("Owner")
async def unlock(ctx):
    """Открывает канал обратно для @everyone"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Канал открыт.")


# ==========================================
# 2. TECHNICAL ADMINISTRATOR (Утилиты и логирование)
# ==========================================

@bot.command()
@commands.has_role("Technical Administrator")
async def ping(ctx):
    """Проверка задержки бота и API"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"📡 Пинг бота: `{latency} мс`")

@bot.command()
@commands.has_role("Technical Administrator")
async def serverinfo(ctx):
    """Детальная техническая инфа о сервере"""
    g = ctx.guild
    embed = disnake.Embed(title=f"Сервер: {g.name}", color=0x5865F2)
    embed.add_field(name="ID Сервера", value=f"`{g.id}`", inline=True)
    embed.add_field(name="Владелец", value=g.owner.mention, inline=True)
    embed.add_field(name="Участников", value=f"`{g.member_count}`", inline=True)
    embed.add_field(name="Текстовых каналов", value=f"`{len(g.text_channels)}`", inline=True)
    embed.add_field(name="Голосовых каналов", value=f"`{len(g.voice_channels)}`", inline=True)
    embed.add_field(name="Количество ролей", value=f"`{len(g.roles)}`", inline=True)
    embed.set_thumbnail(url=g.icon.url if g.icon else None)
    await ctx.send(embed=embed)


# ==========================================
# 3. TRUE FEMBOY (Интерактив и рулетки)
# ==========================================

@bot.command()
@commands.has_role("True Femboy")
async def poll(ctx, question: str, *options):
    """Создать голосовалку (!poll "Заголовок" "Вариант1" "Вариант2")"""
    if len(options) > 10:
        return await ctx.send("❌ Максимум 10 вариантов ответа.")
    if len(options) < 2:
        return await ctx.send("❌ Укажи хотя бы 2 варианта ответа в кавычках.")

    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    description = []
    for i, option in enumerate(options):
        description.append(f"{reactions[i]} {option}")

    embed = disnake.Embed(title=f"📊 {question}", description="\n".join(description), color=0x9b59b6)
    msg = await ctx.send(embed=embed)

    for i in range(len(options)):
        await msg.add_reaction(reactions[i])


# ==========================================
# 4. FEMBOY (Голосовой менеджмент)
# ==========================================

@bot.command()
@commands.has_role("Femboy")
async def drag(ctx, channel: disnake.VoiceChannel):
    """Перетащить всех из текущего голосового канала в другой"""
    if not ctx.author.voice:
        return await ctx.send("❌ Ты должен быть в голосовом канале.")
    
    current_vc = ctx.author.voice.channel
    members = current_vc.members
    
    if not members:
        return await ctx.send("В твоем канале никого нет.")

    for m in members:
        await m.move_to(channel)
    
    await ctx.send(f"Перемещено `{len(members)}` участников в `{channel.name}`.")


# ==========================================
# ОБРАБОТКА ОШИБОК
# ==========================================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"❌ Нет роли `{error.missing_role}`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Не хватает аргументов команды.")

TOKEN = os.getenv("BOT_TOKEN")
if __name__ == "__main__":
    bot.run(TOKEN)