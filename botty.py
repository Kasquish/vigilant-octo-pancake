#Tumble is here to roll dice... and do some other things!

import datetime
import discord
import random
import os
import pickle
import time


from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import Bot

tumble = commands.Bot(command_prefix=".")

chanceList = []
torracatList = []
capsuleList = []
miningList = []
thanksList = []
hiList = []

bot_token = os.environ['BOT_TOKEN']

starttime = datetime.datetime.now()

##last6 = [0,0]
##last3 = [0,0]
##last10 = [0,0]
##last20 = [0,0]

##TODO maybe: have Tumble comment on getting the same roll x times in a row? For fun?


#Helper function
def listFromFile(filename,listy):

    with open(filename,"r") as infile:
        for line in infile:
            line = line.strip()
            if line:
                listy.append(line)


@tumble.event
async def on_ready():

    listFromFile("torracat.txt",torracatList)
    listFromFile("capsule.txt",capsuleList)
    listFromFile("mining.txt",miningList)
    listFromFile("thanks.txt",thanksList)
    listFromFile("hi.txt",hiList)

    for filename in os.listdir("chance"):
        chanceList.append(filename)

    

    

    print("Tumble is ready!")







######################################################
######################   DICE   ######################
######################################################

#####D6#####

@tumble.command(pass_context = True)
async def move(ctx):
    result = random.randint(1,6)
    await tumble.say("From 1-6, you got a...\n[ **"+  str(result)  +"** ]")
    print("Move called!")
    
@tumble.command(pass_context = True)
async def randomroll(ctx):
    result = random.randint(1,6)
    await tumble.say("From 1-6, you got a...\n[ **"+  str(result)  +"** ]")    
    print("Randomroll called!")

#####2D6#####

@tumble.command(pass_context = True)
async def mushroom(ctx):
    result1 = random.randint(1,6)
    result2 = random.randint(1,6)
    sayString = ""
    sayString += "With two dice, you rolled "+str(result1)+" and "+str(result2)+"! The total is...\n"
    sayString += "[ **"+  str(result1+result2)  +"** ]\n"
    if result1 == result2:
        sayString += "*Hey, you got doubles!*"
    await tumble.say(sayString)
    print("Mushroom called!")

@tumble.command(pass_context = True)
async def mega(ctx):
    result1 = random.randint(1,6)
    result2 = random.randint(1,6)
    sayString = ""
    sayString += "With two dice, you rolled "+str(result1)+" and "+str(result2)+"! The total is...\n"
    sayString += "[ **"+  str(result1+result2)  +"** ]\n"
    if result1 == result2:
        sayString += "*Hey, you got doubles!*"
    await tumble.say(sayString)
    print("Mega called!")



#####D3#####

@tumble.command(pass_context = True)
async def halfmove(ctx):
    result = random.randint(1,3)
    await tumble.say("From 1-3, you got a...\n[ **"+  str(result)  +"** ]")
    print("Halfmove called!")
    


#####D10#####
    
@tumble.command(pass_context = True)
async def d10(ctx):
    result = random.randint(1,10)
    await tumble.say("From 1-10, you got a...\n[ **"+  str(result)  +"** ]")
    print("d10 called!")

    

#####D20#####
    
@tumble.command(pass_context = True)
async def d20(ctx):
    result = random.randint(1,20)
    await tumble.say("From 1-20, you got a...\n[ **"+  str(result)  +"** ]")
    if result == 1:
        await tumble.say("*Somewhere, an anvil falls on an Umbreon...*")
        print("They found the Umbreon easter egg!")
    print("d20 called!")



#####D30#####
    
@tumble.command(pass_context = True)
async def d30(ctx):
    result = random.randint(1,30)
    await tumble.say("From 1-30, you got a...\n[ **"+  str(result)  +"** ]")
    print("d30 called!")


#####D50#####
    
@tumble.command(pass_context = True)
async def d50(ctx):
    result = random.randint(1,30)
    await tumble.say("From 1-30, you got a...\n[ **"+  str(result)  +"** ]")
    print("d50 called!")



#####Thwomp#####
    
@tumble.command(pass_context = True)
async def thwomp(ctx):
    thwompList = ["Blue","Green","Violet"]
    sayString = ""
    for color in thwompList:
        result = random.randint(1,3)
        sayString += color+" Thwomp: **"+str(result)+"**\n"
    await tumble.say(sayString)
    print("Thwomp called!")



#####SSLBlock##### The block in Shifting Sand Land that gives 5-30 coins!
    
@tumble.command(pass_context = True)
async def sslblock(ctx):
    result = random.randint(5,30)
    await tumble.say("You bashed the block, and out fell...\n[ **"+  str(result)  +" coins!** ]")
    print("sslblock called!")



######################################################
######################  WHEELS  ######################
######################################################

@tumble.command(pass_context = True)
async def chance(ctx):
    result = random.choice(chanceList)
    await tumble.upload("chance/"+result)
    print("Chance called!")

@tumble.command(pass_context = True)
async def capsule(ctx):
    result = random.choice(capsuleList)
    await tumble.say("You opened the capsule, and found...\n[ **"+  str(result) +"** ]")
    print("Capsule called!")
    
@tumble.command(pass_context = True)
async def torracat(ctx):
    result = random.choice(torracatList)
    await tumble.say("Torracat decrees that the following shall happen!\n[ **"+  str(result)  +"** ]")
    print("Torracat called!")
    
@tumble.command(pass_context = True)
async def mining(ctx):
    result = random.choice(miningList)
    await tumble.say("After some digging, you found...\n[ **"+  str(result)  +"** ]")
    print("Mining called!")



######################################################
######################  EVENTS  ######################
######################################################

@tumble.command(pass_context = True)
async def freegift(ctx):
    if ctx.message.channel.id != "373259889826332673":
        await tumble.say("Please call .freegift in the Trading channel!")
    else:
        idList = []
        listFromFile("freegift_ids.txt",idList)
        if str(ctx.message.author.id) in idList:
            await tumble.say("You already got your free coupon! I only have so many to go around...")
        else:
            ticketList = []
            listFromFile("freegift.txt",ticketList)
            ticket = random.choice(ticketList)
            await tumble.say(
ctx.message.author.name + """, your free coupon is...
the """+ticket+""" Coupon!
Keep this in your items - you can redeem it to play with """+ticket+"""!
Or you can trade it with someone else!""")
            with open("freegift_ids.txt","a") as outFile:
                print(str(ctx.message.author.id),file=outFile)
    print("Freegift called!")


######################################################
###################### ME ONLY  ######################
######################################################

##@tumble.command(pass_context = True)
##async def generalhanasu(ctx):
##    #Tumble says something in general chat.
##    result = random.choice(chanceList)
##    await tumble.upload("chance/"+result)
##    print("Chance called!")    

@tumble.command(pass_context = True)
async def makeafile(ctx):
    if ctx.message.author.id == "161982345207873536":
        outfile = open("testytesty.txt","w")
        print("Booooo!",file=outfile)
        await tumble.say("I tried to do it!")
        outfile.close()
        print("I tried!")
    else:
        await tumble.say("Whoa! How did you know this was a thing? You're not Namadu!")
            

######################################################
######################   MISC   ######################
######################################################
#(for fun, mainly)

@tumble.command(pass_context = True)
async def canikickyou(ctx):
    await tumble.say("Sure thing! Don't worry, it won't hurt or anything.")
    await tumble.say("I hope I can come back for another party, though!")
    print("CanIKickYou called!")

@tumble.command(pass_context = True)
async def annoying(ctx):
    await tumble.say("Aww, really? Sorry to bother you, then!")
    await tumble.say("B-but I'll go teach someone else how to host a party, and bring 'em over!")
    await tumble.say("I hope you have a nice day! :heart:")
    print("Annoying called...")

@tumble.command(pass_context = True)
async def thanks(ctx):
    result = random.choice(thanksList)
    await tumble.say(result)
    print("Thanks called!")

@tumble.command(pass_context = True)
async def hi(ctx):
    
    result = random.choice(hiList)
    await tumble.say(result)
    print("Hi called!")

@tumble.command(pass_context = True)
async def hello(ctx):
    result = random.choice(hiList)
    await tumble.say(result)
    print("Hi called!")
    
@tumble.command(pass_context = True)
async def ping(ctx):
    await tumble.say("Pong! ♪")
    print("Ping called!")

tumble.remove_command('help')

@tumble.command(pass_context = True)
async def help(ctx):
    await tumble.whisper("""Hiiii! I'm Tumble, and I'm here to ensure that your party goes smoothly!
It looks like Cassi Lite can't be around now... I'll do what I can in their place!
Make sure you put a . before making a request for me, so that I know you're talking to me.

---Dice---
halfmove 
move
randomroll
mushroom
mega
d10
d20
d30
d50

---Wheels---
chance: Draws a Chance Card and shows it to everybody!
capsule: This opens a capsule! I wonder what we'll find inside?
mining: Use this to find a random evolution item!
torracat: Um... huh? What's this command? I swear I didn't put it here...

---Other---
help: I do this, silly!
I might understand some other little things you say, too!

Do your best to become the Superstar!
Wait... what kind of party is this again? ...Have fun anyway!
""")
    print("Help called!")




######################################################
##################   WEEKLY QUESTS  ##################
######################################################

WEEKLY_TARGET_CHANNEL = '393628008591917059'



async def updateWeeklyTask():
    nextWeeklyTime = 0
    
    with open("WeeklyTime.pickle","rb") as infile:
        nextWeeklyTime = pickle.load(infile)


    currDate = datetime.datetime.now()

    
    if nextWeeklyTime <= currDate:

        weeklyString = ""
        randomWeekly1 = []

        listFromFile("WeeklyPool.txt",randomWeekly1)

        weeklyString = random.choice(randomWeekly1)

        leftBracket = weeklyString.find('[')
        
        if weeklyString.find('[') != -1:
            rightBracket = weeklyString.find(']')
            partToReplace = weeklyString[leftBracket:rightBracket+1]
            partFilename = partToReplace.strip('[]')

            randomWeekly2 = []

            listFromFile("Weekly"+partFilename+".txt",randomWeekly2)

            weeklyString = weeklyString.replace(partToReplace,random.choice(randomWeekly2))

        currWeekly = weeklyString

        with open("WeeklyCurrent.txt","w") as outfile:
            print(currWeekly,file=outfile)


        while nextWeeklyTime <= currDate:
            nextWeeklyTime += datetime.timedelta(days = 7)
        
        with open("WeeklyTime.pickle","wb") as outfile:
            pickle.dump(nextWeeklyTime,outfile)

        targetChannel = discord.Object(id = WEEKLY_TARGET_CHANNEL);

        await sendWeeklyMessage(targetChannel);
            
            


async def sendWeeklyMessage(channel):

    with open("WeeklyCurrent.txt","r") as infile:
        currWeekly = infile.readline().strip()

    with open("WeeklyTime.pickle","rb") as infile:
        nextWeeklyTime = pickle.load(infile)
        
    dateString = nextWeeklyTime.strftime("%B %d!")
    wholeMessage = "Current task:\n"+currWeekly+"\nFinish by the end of "+str(dateString)
    await tumble.send_message(channel,wholeMessage)





##@tumble.command(pass_context = True)
##async def weekly(ctx):
##    await sendWeeklyMessage(ctx.message.channel);
    
    

######################################################
#################   BACKGROUND TASK  #################
######################################################
#primarily for weekly reminders

BG_TASK_INTERVAL = 300; #In seconds, how long the background task should sleep.

async def background_task():
    await tumble.wait_until_ready()

    while not tumble.is_closed:

        #Get runtime, minus microseconds.
        runtime = datetime.datetime.now() - starttime
        runtime -= datetime.timedelta(microseconds = runtime.microseconds)

        await updateWeeklyTask()

        await sleep(BG_TASK_INTERVAL)


tumble.loop.create_task(background_task())

tumble.run(bot_token)
