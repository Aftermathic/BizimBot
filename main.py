import os
from PIL import Image, ImageDraw, ImageFont
import asyncio
import time as t
import random
from replit import db

from keep_active import keep_alive

import discord
from discord.ext import commands

with open("error.txt", "w") as f:
    f.write("")

client = discord.Client()
bot = commands.Bot(command_prefix='<')

def addText(text):
    if "randText" in db.keys():
        texts = db["randText"]
        texts.append(text)

        db["randText"] = texts
    else:
        texts = []
        texts.append(text)

        db["randText"] = texts

def getNumTexts():
    if "randText" in db.keys():
        all_texts = db["randText"]
        num = len(all_texts)
        
        return num
    else:
        return 0

def getText(number):
    if "randText" in db.keys():
        allTexts = db["randText"]
        try:
            return allTexts[number]
        except:
            return "Debugger: There isn't any text."
    else:
        return ["...", "There isn't any!"][number]

def addTokens(userid, amount):
    if str(userid) + "_tokens" in db.keys():
        usertokens = db[str(userid) + "_tokens"]
        usertokens += amount

        db[str(userid) + "_tokens"] = usertokens
    else:
        db[str(userid) + "_tokens"] = 0
        usertokens = db[str(userid) + "_tokens"]
        usertokens += amount

        db[str(userid) + "_tokens"] = usertokens

def subtractTokens(userid, amount):
    if str(userid) + "_tokens" in db.keys():
        usertokens = db[str(userid) + "_tokens"]
        usertokens -= amount

        db[str(userid) + "_tokens"] = usertokens
    else:
        db[str(userid) + "_tokens"] = 0
        usertokens = db[str(userid) + "_tokens"]
        usertokens -= amount

        if usertokens <= 0:
            usertokens = 0

        db[str(userid) + "_tokens"] = usertokens

def getTokens(userid):
    if str(userid) + "_tokens" in db.keys():
        return db[str(userid) + "_tokens"]
    else:
        db[str(userid) + "_tokens"] = 0
        return db[str(userid) + "_tokens"]

def addLevels(userid, amount):
    if str(userid) + "_levels" in db.keys():
        userlevels = db[str(userid) + "_levels"]
        userlevels += amount

        db[str(userid) + "_levels"] = userlevels
    else:
        db[str(userid) + "_levels"] = 0
        userlevels = db[str(userid) + "_levels"]
        userlevels += amount

        db[str(userid) + "_levels"] = userlevels

def getLevels(userid):
    if str(userid) + "_levels" in db.keys():
        return db[str(userid) + "_levels"]
    else:
        db[str(userid) + "_levels"] = 0
        return db[str(userid) + "_levels"]

@bot.command()
async def sourceCode(ctx):
    await ctx.send("Here is the source code: <https://github.com/Aftermathic/BizimBot>")

@bot.command()
async def slots(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author

    symbols = [":grapes:", ":cherries:", ":lemon:", ":green_apple:", ":kiwi:", ":peach:"]

    row1 = []
    row2 = []
    row3 = []

    await ctx.send('Enter your bet!')

    try:
        bet = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send('You took too long to enter your bet.')
    except:
        await ctx.send("Something went wrong.")
    else:
        try:
            int(bet.content)
        except ValueError:
            await ctx.send("Your bet wasn't a number...")
        except:
            await ctx.send("Something went wrong...")
        else:
            await ctx.send("Rolling...")

            for i in range(3):
                row1.append(random.choice(symbols))

            for i in range(3):
                row2.append(random.choice(symbols))

            for i in range(3):
                row3.append(random.choice(symbols))

            t.sleep(5)

            if row1[0] == row1[1] and row1[1] == row1[2] or row2[0] == row2[1] and row2[1] == row2[2] or row3[0] == row3[1] and row3[1] == row3[2]:
                await ctx.send(row1[0] + row1[1] + row1[2] + "\n" + row2[0] + row2[1] + row2[2] + '\n' + row3[0] + row3[1] + row3[2] + "\n\nYou won! Your reward would have been **" + str(int(bet.content)) + "** if this wasn't just a simulation!")
                print("sideways win")

            elif row1[0] == row2[0] and row2[0] == row3[0] or row1[1] == row2[1] and row2[1] == row3[1] or row2[2] == row2[2] and row2[2] == row3[2]:
                await ctx.send(row1[0] + row1[1] + row1[2] + "\n" + row2[0] + row2[1] + row2[2] + '\n' + row3[0] + row3[1] + row3[2] + "\n\nYou won! Your reward would have been **" + str(int(bet.content)) + "** if this wasn't just a simulation!")
                print("downward win")

            elif row1[0] == row2[1] and row2[1] == row3[2] or row1[2] == row2[1] and row2[1] == row3[0]:
                await ctx.send(row1[0] + row1[1] + row1[2] + "\n" + row2[0] + row2[1] + row2[2] + '\n' + row3[0] + row3[1] + row3[2] + "\n\nYou won! Your reward would have been **" + str(int(bet.content)) + "** if this wasn't just a simulation!")
                print("crossed win")
            else:
                await ctx.send(row1[0] + row1[1] + row1[2] + "\n" + row2[0] + row2[1] + row2[2] + '\n' + row3[0] + row3[1] + row3[2] + "\n\nYou lost. Your reward would have been **" + str(int(bet.content)) + "** if this wasn't just a simulation.")

@bot.command()
async def math(ctx):
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
        elif sign == 5:
            equation = str(a) + " % " + str(b)

        return equation

    await ctx.send("What subject would you like? (Please choose with a number.)\n\n1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Modulus")

    try:
        option = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send('You took too long to enter your answer.')
    except:
        await ctx.send("Something went wrong.")
    else:
        try:
            int(option.content)
        except:
            await ctx.send("Something went wrong. We will choose your subject for you.")
            operation = random.randint(1, 5)
        else:
            operation = int(option.content)

    reward_amount = random.randint(5, 25)

    t.sleep(1)

    if operation == 1:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        sum = a + b

        equation = generateEquation(a, b, 1)

        await ctx.send("What is " + equation + "?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to enter your answer.')
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Your answer isn't a number.")
            except:
                await ctx.send("Something went wrong.")
            else:
                if answer.content == str(sum):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Good job! You got rewarded " + str(reward_amount) + " tokens!")
                else:
                    await ctx.send("Sorry, the sum was " + str(sum) + ".")
    if operation == 2:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        difference = a - b

        equation = generateEquation(a, b, 2)

        await ctx.send("What is " + equation + "?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to enter your answer.')
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Your answer isn't a number.")
            except:
                await ctx.send("Something went wrong.")
            else:
                if answer.content == str(difference):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Good job! You got rewarded " + str(reward_amount) + " tokens!")
                else:
                    await ctx.send("Sorry, the difference was " + str(difference) + ".")
    if operation == 3:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        product = a * b

        equation = generateEquation(a, b, 3)

        await ctx.send("What is " + equation + "?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to enter your answer.')
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Your answer isn't a number.")
            except:
                await ctx.send("Something went wrong.")
            else:
                if answer.content == str(product):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Good job! You got rewarded " + str(reward_amount) + " tokens!")
                else:
                    await ctx.send("Sorry, the product was " + str(product) + ".")
                    
    if operation == 4:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        while a % b != 0 and a != b:
            b = random.randint(1, 100)

        quotient = a / b

        equation = generateEquation(a, b, 4)

        await ctx.send("What is " + equation + "?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to enter your answer.')
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Your answer isn't a number.")
            except:
                await ctx.send("Something went wrong.")
            else:
                if answer.content == str(int(quotient)):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Good job! You got rewarded " + str(reward_amount) + " tokens!")
                else:
                    await ctx.send("Sorry, the quotient was " + str(quotient) + ".")
    if operation == 5:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

        while a < b:
            a = random.randint(1, 100)

        quotient = a % b

        equation = generateEquation(a, b, 5)

        await ctx.send("What is " + equation + "?")
        
        try:
            answer = await bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to enter your answer.')
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                int(answer.content)
            except ValueError:
                await ctx.send("Your answer isn't a number.")
            except:
                await ctx.send("Something went wrong.")
            else:
                if answer.content == str(int(quotient)):
                    addTokens(ctx.author.id, reward_amount)
                    await ctx.send("Good job! You got rewarded " + str(reward_amount) + " tokens!")
                else:
                    await ctx.send("Sorry, the quotient was " + str(int(quotient)) + ".")

@bot.command()
async def coinFlip(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
    await ctx.send("What will you bet for?\nHeads (1), or Tails (2) ?\nAnswer using the number next to the options.")
    
    try:
        answer = await bot.wait_for('message', check=check, timeout=15.0)
        option = int(answer.content)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you took too long.")
    except:
        await ctx.send("Your answer was invalid.")
    else:
        reward = random.randint(5, 15)
        loss_amount = random.randint(5, 15)
        
        if option in (1, 2):
            coin_side = random.randint(1, 2)
            if coin_side == option:
                addTokens(ctx.author.id, reward)
                await ctx.send(f"You won! You earned {reward} tokens!")
            else:
                subtractTokens(ctx.author.id, loss_amount)
                await ctx.send(f"You lost. You lost {loss_amount} tokens.")
        else:
            await ctx.send("Your option is invalid.")
    
@bot.command()
async def getLevelCost(ctx):
    cost = getLevels(ctx.author.id) * 125
    await ctx.send("You need " + str(cost) + " tokens.")

@bot.command()
async def levelUp(ctx):
    cost = getLevels(ctx.author.id) * 125
    usertokens = getTokens(ctx.author.id)

    if usertokens >= cost:
        addLevels(ctx.author.id, 1)
        subtractTokens(ctx.author.id, cost)

        newlv = getLevels(ctx.author.id)

        await ctx.send("You have leveled up to level " + str(newlv) + "!")
    else:
        await ctx.send("You don't have enough money to level up. You need " + str(cost - usertokens) + " more tokens.")

@bot.command()
async def myLevels(ctx):
    base = Image.open("images/levelstemplate.png").convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))

    fnt = ImageFont.truetype("fonts/SEGOEUI.TTF", 32)

    d = ImageDraw.Draw(txt)

    d.text((65,10), ctx.author.display_name, font=fnt, fill=(255,255,255,255))
    d.text((141,100), str(getLevels(ctx.author.id)), font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)
    out.save("images/levelstemplate_edited.png")

    await ctx.send(file=discord.File("images/levelstemplate_edited.png"))

@bot.command()
async def myTokens(ctx):
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
async def getRandomText(ctx):
    num = random.randint(0, getNumTexts() - 1)
    await ctx.send(f"{num}. {getText(num)}")

@bot.command()
async def addRandomText(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
        
    await ctx.send("Enter the text!")
        
    try:
        text = await bot.wait_for('message', check=check, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send('You took too long to enter your text.')
    else:
        addText(f"{text.content}\n**From: {ctx.author}**")
        await ctx.send("Your text has been added.")

@bot.command()
async def showAllRandText(ctx):
    text = ""
    num = 0
    while num < getNumTexts():
        string = f"{num}. {getText(num)}"
        string += "\n\n"

        text += string
        num += 1
        
    await ctx.send(text)
        
@bot.command()
async def botStatus(ctx):
    await ctx.send("You can see the status here: https://BizimBot.aftermathtaken.repl.co")

@bot.command()
async def deleteRandText(ctx):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author == ctx.author
        
    member = ctx.message.author
    
    liderler = discord.utils.get(member.guild.roles, name="Liderler")
    mod_role = discord.utils.get(member.guild.roles, name="Moderatör")
    
    if member.roles in [liderler, mod_role] or member.id == 751206285680181434:
        await ctx.send("Which one would you like to delete? (You must enter what number the text is)")
        try:
            number = await bot.wait_for('message', check=check, timeout=15.0)
            int(number.content)
        except asyncio.TimeoutError:
            await ctx.send("You took too long.")
        except ValueError:
            await ctx.send("Your text number isn't a number.")
        except:
            await ctx.send("Something went wrong.")
        else:
            try:
                db["randText"][int(number.content)]
            except:
                await ctx.send("Your number is invalid.")
            else:
                del db["randText"][int(number.content)]
                await ctx.send(f"Deleted text number {number.content}.")
    else:
        await ctx.send("You cannot use this command.")

"""
@bot.command()
async def deleteAllRandTexts(ctx):
    await ctx.send("resetting all random texts for updates.")
    db["randText"] = []
"""

keep_alive()

try:
    try:
        bot.run(os.environ['bot_token'])
    except:
        token = open("token.txt", "r")
        bot.run(token.read())
except Exception as e:
    with open("error.txt", "w") as f:
        f.write(f"{e}")