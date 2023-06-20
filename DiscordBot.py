import discord
import datetime
import requests
from discord.ext import commands, tasks


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    print(f"Estou pronto! Conectado como {bot.user}")
    # current_time.start()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "palavrão" in message.content:
        await message.channel.send(f"Por favor, {message.author.name}, não fale palavrão aqui!")

        await message.delete()

    await bot.process_commands(message)


@bot.command(name="oi")
async def send_hello(ctx):
    name = ctx.author.name

    responde = "Olá, " + name

    await ctx.send(responde)


@bot.command(name="regras")
async def send_rulles(ctx):
    name = ctx.author.name
    regras = "Olá, " + name + " as regras são:"

    await ctx.send(regras)


@bot.command(name="calcular")
async def calculate_expression(ctx, *expression):
    expression = "".join(expression)
    print(expression)
    resposta = eval(expression)

    await ctx.send("A resposta é: " + str(resposta))


@bot.command()
async def binance(ctx, coin, base):
    try:
        resposta = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")

        data = resposta.json()
        preco = data.get("price")

        if preco:
            await ctx.send(f"O valor do {coin} para {base} é {preco}")
        else:
            await ctx.send(f"O valor do {coin} para {base} é inválido")
    except Exception as error:
        await ctx.send("Ops... Deu algum erro!")
        print(error)


@tasks.loop(seconds=10)
async def current_time():
    time = datetime.datetime.now()
    time = time.strftime("%d/%m/%Y às %H:%M%S")

    channel = bot.get_channel(786017079492345876)

    await channel.send("Data atual: " + time)


bot.run('MTEyMDQyMDk0MDUwMTc2NjI2NA.G5knp-.SdTCtO5WlXcpHAOEbtFAz_tS5NpZNTzrR8WIzI')
