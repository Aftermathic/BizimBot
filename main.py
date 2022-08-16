import os
from PIL import Image, ImageDraw, ImageFont
import asyncio
import time as t
import random
from replit import db

from keep_active import keep_alive

import discord
from discord.ext import commands

maxlevel = 1000
maxtokens = 50000

cost_multiplier = 25

with open("error.txt", "w") as f:
    f.write("")

client = discord.Client()
bot = commands.Bot(command_prefix='<')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Bu komutun bir bekleme süresi var, komutu {round(error.retry_after, 2)} saniye sonra kullanabilirsin.')

def addText(text):
    if "Rmetin" in db.keys():
        texts = db["Rmetin"]
        texts.append(text)

        db["Rmetin"] = texts
    else:
        texts = []
        texts.append(text)

        db["Rmetin"] = texts

def getNumTexts():
    if "Rmetin" in db.keys():
        all_texts = db["Rmetin"]
        num = len(all_texts)
        
        return num
    else:
        return 0

def getText(number):
    if "Rmetin" in db.keys():
        allTexts = db["Rmetin"]
        try:
            return allTexts[number]
        except:
            return "Debugger: Hiçbir metin yok."
    else:
        return "Debugger: Hiçbir metin yok."

def addTokens(userid, amount):
    if str(userid) + "_jetonlar" in db.keys():
        usertokens = db[str(userid) + "_jetonlar"]
        usertokens += amount

        db[str(userid) + "_jetonlar"] = usertokens
    else:
        db[str(userid) + "_jetonlar"] = 0
        usertokens = db[str(userid) + "_jetonlar"]
        usertokens += amount

        db[str(userid) + "_jetonlar"] = usertokens

def subtractTokens(userid, amount):
    if str(userid) + "_jetonlar" in db.keys():
        usertokens = db[str(userid) + "_jetonlar"]
        usertokens -= amount

        db[str(userid) + "_jetonlar"] = usertokens
    else:
        db[str(userid) + "_jetonlar"] = 0
        usertokens = db[str(userid) + "_jetonlar"]
        usertokens -= amount

        if usertokens <= 0:
            usertokens = 0

        db[str(userid) + "_jetonlar"] = usertokens

def getTokens(userid):
    if str(userid) + "_jetonlar" in db.keys():
        if db[str(userid) + "_jetonlar"] > maxtokens:
            db[str(userid) + "_jetonlar"] = maxtokens
            
        return db[str(userid) + "_jetonlar"]
    else:
        db[str(userid) + "_jetonlar"] = 0
        return db[str(userid) + "_jetonlar"]

def addLevels(userid, amount):
    if str(userid) + "_seviyeler" in db.keys():
        userlevels = db[str(userid) + "_seviyeler"]
        userlevels += amount

        db[str(userid) + "_seviyeler"] = userlevels
    else:
        db[str(userid) + "_seviyeler"] = 0
        userlevels = db[str(userid) + "_seviyeler"]
        userlevels += amount

        db[str(userid) + "_seviyeler"] = userlevels

def getLevels(userid):
    if str(userid) + "_seviyeler" in db.keys():
        if db[str(userid) + "_seviyeler"] >= maxlevel:
            db[str(userid) + "_seviyeler"] = maxlevel
            
        return db[str(userid) + "_seviyeler"]
    else:
        db[str(userid) + "_seviyeler"] = 0
        return db[str(userid) + "_seviyeler"]

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def matematik(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author

    def generateEquation(a, b, sign):
        if sign == 1:
            equation = str(a) + " + " + str(b)
        elif sign == 2:
            equation = str(a) + " - " + str(b)
        elif sign == 3:
            equation = str(a) + " x " + str(b)
        elif sign == 4:
            equation = str(a) + " ÷ " + str(b)

        return equation

    await ctx.send("Ne işlemi yapmak istiyorsun? (Lütfen sayısını belirt.)\n\n1. Toplama\n2. Çıkarma\n3. Çarpma\n4. Bölme")

    try:
        option = await bot.wait_for('message', check=check, timeout=10.0)
    except asyncio.TimeoutError:
        await ctx.send('Cevap vermen çok uzun sürdü.')
    except:
        await ctx.send("Bir şeyler ters gitti.")
    else:
        try:
            int(option.content)
        except:
            await ctx.send("Bir şeyler ters gitti. Senin için işlemi ben seçiyorum.")
            operation = random.randint(1, 4)
        else:
            operation = int(option.content)

    reward_amount = random.randint(4, 10)

    t.sleep(1)

    if operation == 1:
        a = random.randint(1, 20)
        b = random.randint(1, 20)

        sum = a + b

        equation = generateEquation(a, b, 1)

        await ctx.send("İşte soru: " + equation + " nedir?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send('Cevap vermen çok uzun sürdü.')
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Cevabın bir sayı değil.")
            except:
                await ctx.send("Bir şeyler ters gitti.")
            else:
                if answer.content == str(sum):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Güzel! " + str(reward_amount) + " tane jeton kazandın!")
                else:
                    await ctx.send("Üzgünüm, cevap şuydu: " + str(sum) + ".")
    if operation == 2:
        a = random.randint(1, 20)
        b = random.randint(1, 20)

        difference = a - b

        equation = generateEquation(a, b, 2)

        await ctx.send("İşte soru " + equation + " nedir?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send('Cevap vermen çok uzun sürdü.')
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Cevabın bir sayı değil.")
            except:
                await ctx.send("Bir şeyler ters gitti.")
            else:
                if answer.content == str(difference):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Güzel! " + str(reward_amount) + " tane jeton kazandın!")
                else:
                    await ctx.send("Üzgünüm, cevap şuydu: " + str(difference) + ".")
    if operation == 3:
        a = random.randint(1, 20)
        b = random.randint(1, 20)

        product = a * b

        equation = generateEquation(a, b, 3)

        await ctx.send("İşte soru " + equation + " nedir?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send('Cevap vermen çok uzun sürdü.')
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Cevabın bir sayı değil.")
            except:
                await ctx.send("Bir şeyler ters gitti.")
            else:
                if answer.content == str(product):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Güzel! " + str(reward_amount) + " tane jeton kazandın!")
                else:
                    await ctx.send("Üzgünüm, cevap şuydu: " + str(product) + ".")
                    
    if operation == 4:
        a = random.randint(1, 20)
        b = random.randint(1, 20)

        while a % b != 0 and a != b:
            b = random.randint(1, 20)

        quotient = a / b

        equation = generateEquation(a, b, 4)

        await ctx.send("İşte soru " + equation + " nedir?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('Cevap vermen çok uzun sürdü.')
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Cevabın bir sayı değil.")
            except:
                await ctx.send("Bir şeyler ters gitti.")
            else:
                if answer.content == str(int(quotient)):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Güzel! " + str(reward_amount) + " tane jeton kazandın!")
                else:
                    await ctx.send("Üzgünüm, cevap şuydu: " + str(quotient) + ".")

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def yazıtura(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
    await ctx.send("Yazı mı tura mı?\nYazı (1), Tura (2) ?\nCevabını sayıya göre seç.")
    
    try:
        answer = await bot.wait_for('message', check=check, timeout=5.0)
        option = int(answer.content)
    except asyncio.TimeoutError:
        await ctx.send("Cevap vermen uzun sürdü.")
    except:
        await ctx.send("Cevabın geçersiz.")
    else:
        reward = random.randint(20, 35)
        loss_amount = random.randint(20, 35)
        
        if option in (1, 2):
            coin_side = random.randint(1, 2)
            if coin_side == option:
                addTokens(ctx.author.id, reward)
                await ctx.send(f"Kazandın! {reward} jeton kazandın!")
            else:
                subtractTokens(ctx.author.id, loss_amount)
                await ctx.send(f"Kaybettin. {loss_amount} jeton kaybettin.")
        else:
            await ctx.send("Cevabın geçersiz.")

@bot.command()
async def yardım(ctx):
    commands = [c.name for c in bot.commands]
    string = "\n\n"
    for i in range(len(commands)):
        string += commands[i] + "\n"
        
    await ctx.send(f"-İşte tüm komutlar: {string}")

@bot.command()
async def kaynakkodu(ctx):
    await ctx.send("Kaynak kodu burada: <https://github.com/Aftermathic/BizimBot>")
    
@bot.command()
async def seviyebedeli(ctx):
    if getLevels(ctx.author.id) >= maxlevel:
        await ctx.send(f"You have already reached the max level of {maxlevel}.")
    else:
        cost = getLevels(ctx.author.id) * cost_multiplier
        await ctx.send("Bir sonraki seviye için " + str(cost) + " tane jetona ihtiyacın var.")

@bot.command()
async def seviyeatla(ctx):
    cost = getLevels(ctx.author.id) * cost_multiplier
    usertokens = getTokens(ctx.author.id)

    if getLevels(ctx.author.id) >= maxlevel:
        await ctx.send(f"You have already reached the max level of {maxlevel}.")
    else:
        if usertokens >= cost:
            addLevels(ctx.author.id, 1)
            subtractTokens(ctx.author.id, cost)

            newlv = getLevels(ctx.author.id)

            await ctx.send("Seviye atladın! Artık " + str(newlv) + ". seviyedesin!")
        else:
            await ctx.send("Seviye atlayabilmek için yeterli jetonun yok. " + str(cost - usertokens) + " tane daha jetona ihtiyacın var.")

@bot.command()
async def levelUpMax(ctx):
    cost = getLevels(ctx.author.id) * cost_multiplier
    usertokens = getTokens(ctx.author.id)

    counter = 0
    
    if getLevels(ctx.author.id) >= maxlevel:
        await ctx.send(f"You have already reached the max level of {maxlevel}.")
    else:
        gettingMaxCost = True
        while gettingMaxCost:
            level = getLevels(ctx.author.id) + counter
            cost = level * cost_multiplier

            if cost >= usertokens:
                gettingMaxCost = False
                counter - 1
            elif level >= 1000:
                level = 1000
            else:
                counter += 1

        cost = level * cost_multiplier
        if counter <= 0:
            await ctx.send("You do not have enough tokens to level up.")
        else:
            subtractTokens(ctx.author.id, cost)
            addLevels(ctx.author.id, counter)
            await ctx.send(f"You leveled up {counter} times!\nYou are now Level {getLevels(ctx.author.id)}!")
        
@bot.command()
async def seviye(ctx):
    base = Image.open("images/levelstemplate.png").convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))

    if getLevels(ctx.author.id) == maxlevel:
        leveltxt = str(getLevels(ctx.author.id)) + " Max Level"
    else:
        leveltxt = str(getLevels(ctx.author.id))

    fnt = ImageFont.truetype("fonts/SEGOEUI.TTF", 32)

    d = ImageDraw.Draw(txt)

    d.text((65,10), ctx.author.display_name, font=fnt, fill=(255,255,255,255))
    d.text((141,100), leveltxt, font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)
    out.save("images/levelstemplate_edited.png")

    await ctx.send(file=discord.File("images/levelstemplate_edited.png"))

@bot.command()
async def jeton(ctx):
    base = Image.open("images/tokenstemplate.png").convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))

    fnt = ImageFont.truetype("fonts/SEGOEUI.TTF", 32)

    d = ImageDraw.Draw(txt)

    d.text((65,10), ctx.author.display_name, font=fnt, fill=(255,255,255,255))
    d.text((141,100), str(getTokens(ctx.author.id)), font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)
    out.save("images/tokenstemplate_edited.png")

    await ctx.send(file=discord.File("images/tokenstemplate_edited.png"))

@bot.command()
async def rastgelemetin(ctx):
    num = random.randint(0, getNumTexts() - 1)
    await ctx.send(f"Random Text Number: {num}\n{getText(num)}")

@bot.command()
async def rastgelemetinekle(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
        
    usertokens = getTokens(ctx.author.id)

    if usertokens >= 2800:
        await ctx.send("Metni gir!")
        
        try:
            text = await bot.wait_for('message', check=check, timeout=35.0)
        except asyncio.TimeoutError:
            await ctx.send('Metni girmen çok uzun sürdü.')
        else:
            subtractTokens(ctx.author.id, 2800)
            addText(f"{text.content}\n**From: {ctx.author}**")
            await ctx.send("Yazdığın metin eklendi.")
    else:
        await ctx.send(f"{2800 - usertokens} tane daha jetona ihtiyacın var.")

@bot.command()
async def rastgelemetinler(ctx):
    text = ""
    num = 0
    while num < getNumTexts():
        string = f"Random Text Number: {num}\n{getText(num)}"
        string += "\n\n"

        text += string
        num += 1
        
    await ctx.send(text)
        
@bot.command()
async def botdurumu(ctx):
    await ctx.send("Botun durumuna buradan bakabilirsin: https://BizimBot.aftermathtaken.repl.co")

@bot.command()
async def rastgelemetinsil(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
        
    member = ctx.message.author

    can_access = False
    
    role_ids = [
        810221843746390056,
        810231463408173127,
        818190484006633503,
        888480560182358077,
        837291848136654878,
        912372948722122803,
        925451222637498448,
        820284664534532126
    ]
    
    for r in member.roles:
        if r.id in role_ids:
            can_access = True
            
    if can_access:
        await ctx.send("Hangisini sileceksin? (Silmek istediğin metnin sayısını gir.)")
        try:
            number = await bot.wait_for('message', check=check, timeout=15.0)
            int(number.content)
        except asyncio.TimeoutError:
            await ctx.send("Cevap vermen uzun sürdü.")
        except ValueError:
            await ctx.send("Yazdığın şey bir sayı değil.")
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            try:
                db["Rmetin"][int(number.content)]
            except:
                await ctx.send("Yazdığın sayı geçersiz.")
            else:
                del db["Rmetin"][int(number.content)]
                await ctx.send(f"{number.content} numaralı metin başarıyla silindi.")
    elif can_access != True:
        await ctx.send("Bu komutu kullanamazsın.")
        
@bot.command()
async def jetonazalt(ctx, user: discord.User):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author

    can_access = False
    member = ctx.message.author
    
    role_ids = [
        810221843746390056,
        810231463408173127,
        818190484006633503,
        888480560182358077,
        837291848136654878,
        912372948722122803,
        925451222637498448,
        820284664534532126
    ]
    
    for r in member.roles:
        if r.id in role_ids:
            can_access = True
            
    if can_access:
        await ctx.send("Ne kadar jeton azaltmak istiyorsun?")
        try:
            number = await bot.wait_for('message', check=check, timeout=15.0)
            int(number.content)
        except asyncio.TimeoutError:
            await ctx.send("Cevap vermen uzun sürdü.")
        except ValueError:
            await ctx.send("Yazdığın şey bir sayı değil.")
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            subtractTokens(user.id, int(number.content))
            await ctx.send("İşlem tamamlandı.")
            
    elif can_access != True:
        await ctx.send("Bu komutu kullanamazsın.")

@bot.command()
async def jetonekle(ctx, user: discord.User):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author

    can_access = False
    member = ctx.message.author
    
    role_ids = [
        810221843746390056,
        810231463408173127,
        818190484006633503,
        888480560182358077,
        837291848136654878,
        912372948722122803,
        925451222637498448,
        820284664534532126
    ]
    
    for r in member.roles:
        if r.id in role_ids:
            can_access = True

    if ctx.author.id == 751206285680181434:
        can_access = True
            
    if can_access:
        await ctx.send("Ne kadar jeton eklemek istiyorsun?")
        
        try:
            number = await bot.wait_for('message', check=check, timeout=15.0)
            int(number.content)
        except asyncio.TimeoutError:
            await ctx.send("Cevap vermen uzun sürdü.")
        except ValueError:
            await ctx.send("Yazdığın şey bir sayı değil.")
        except:
            await ctx.send("Bir şeyler ters gitti.")
        else:
            addTokens(user.id, int(number.content))
            await ctx.send("İşlem tamamlandı.")
            
    elif can_access != True:
        await ctx.send("Bu komutu kullanamazsın.")

#help
keep_alive()

try:
    try:
        bot.run(os.environ['bot_jetonu'])
    except:
        token = open("token.txt", "r")
        bot.run(token.read())
except Exception as e:
    with open("error.txt", "w") as f:
        f.write(f"{e}")