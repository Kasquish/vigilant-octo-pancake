#Samba is here to roll dice... and do some other things!

import datetime
import discord
import random
import os
import pickle
import time

import sys, traceback


from asyncio import sleep
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix=".")

#Lists of strings, from randomWheels.
torracatList = []
capsuleList = []
miningList = []

randomitemList = []

spacebonusList = []
flatbonusList = []
otherbonusList = []

#Lists of quotes, from randomTalk.

thanksList = []
hiList = []

#Lists of image names, from their respective folders.
chanceList = []
malieStarList = []

#Used to make a repeated Star location less likely.
#Not guaranteed to work, as bot may restart occasionally.
prevStarLoc = [-1]

#Gets the bot token straight from heroku. You can't see it!
bot_token = os.environ['BOT_TOKEN']

#So we can check bot's uptime.
starttime = datetime.datetime.now()

##last6 = [0,0]
##last3 = [0,0]
##last10 = [0,0]
##last20 = [0,0]

##TODO maybe: have Samba comment on getting the same roll x times in a row? For fun?


#Helper function
def listFromFile(filename,listy):

    with open(filename,"r") as infile:
        for line in infile:
            line = line.strip()
            if line:
                listy.append(line)











#TODO: update discord.py to version 1.0 so this actually works!
#Please disregard all this commented-out stuff.
###If you want to add more command files in the commands folder,
###add them here too, so the bot can properly load them. :3
                
##initial_extensions = ['commands.testCommand']
##
##if __name__ == '__main__':
##    for extension in initial_extensions:
##        try:
##            bot.load_extension(extension)
##        except Exception as e:
##            print('Failed to load extension {extension}.', file=sys.stderr)
##            traceback.print_exc()


@bot.event
async def on_ready():

    print("Preparing lists...")
    listFromFile("randomWheels/torracat.txt",torracatList)
    listFromFile("randomWheels/capsule.txt",capsuleList)
    listFromFile("randomWheels/mining.txt",miningList)
    
    listFromFile("randomTalk/thanks.txt",thanksList)
    listFromFile("randomTalk/hi.txt",hiList)
    
    listFromFile("randomWheels/randomitem.txt",randomitemList)
    
    listFromFile("randomWheels/spacebonus.txt",spacebonusList)
    listFromFile("randomWheels/otherbonus.txt",otherbonusList)
    listFromFile("randomWheels/flatbonus.txt",flatbonusList)

    for filename in os.listdir("chance"):
        chanceList.append(filename)
    for filename in os.listdir("maliestar"):
        malieStarList.append(filename)
    print("Lists prepared!")

    prevStarLoc = 0

    

    print("Samba is ready!")

    print(discord.__version__)




######################################################
######################   DICE   ######################
######################################################

#####D#####

@bot.command(pass_context = True, name = "roll", aliases = ["d"])
async def roll(ctx,*args):
    if len(args) > 0:
        arg = args[0].strip("d")
    else:
        arg = "6"
    if arg == "":
        arg = "6"
    try:
        num = int(arg)
        result = random.randint(1,num)
        await bot.say("From 1-"+str(num)+", you got a...\n[ **"+  str(result)  +"** ]")
    except ValueError:
        await bot.say("I-I don't have any dice like that...")
    print("Roll called with " + arg + "!")

#####D6#####

@bot.command(pass_context = True, name = "move", aliases = ["randomroll","d6","6d","curry","curryroll","rollasixsideddiepleasesamba"])
async def move(ctx):
    result = random.randint(1,6)
    await bot.say("From 1-6, you got a...\n[ **"+  str(result)  +"** ]")
    print("Move called!")

#####2D6#####

@bot.command(pass_context = True, name = "mushroom", aliases = ["mega","mush","megamush","megamushroom","2d6","doubleroll","doublemove"])
async def mushroom(ctx):
    result1 = random.randint(1,6)
    result2 = random.randint(1,6)
    sayString = ""
    sayString += "With two dice, you rolled "+str(result1)+" and "+str(result2)+"! The total is...\n"
    sayString += "[ **"+  str(result1+result2)  +"** ]\n"
    if result1 == result2:
        sayString += "*Hey, you got doubles!*"
    await bot.say(sayString)
    print("Mushroom called!")


#####D2#####

@bot.command(pass_context = True, name = "d2")
async def d2(ctx):
    result = random.randint(1,2)
    await bot.say("From 1-2, you got a...\n[ **"+  str(result)  +"** ]")
    print("d2 called!")    
    
#####COINFLIP#####


@bot.command(pass_context = True, name = "coinflip", aliases = ["flipcoin"])
async def coinflip(ctx):
    result = random.choice(("Heads","Tails"))
    await bot.say("The coin came up...\n[ **"+  str(result)  +"** ]")
    print("coinflip called!")    
    
#####D3#####

@bot.command(pass_context = True, name = "halfmove", aliases = ["halfroll","half","d3","mini","minimush","minimushroom"])
async def halfmove(ctx):
    result = random.randint(1,3)
    await bot.say("From 1-3, you got a...\n[ **"+  str(result)  +"** ]")
    print("Halfmove called!")

#####D10#####
    
@bot.command(pass_context = True, name = "d10", aliases = ["grape","grapes","graperoll","grapesroll","cupcake","cupcakes","cupcakeroll","cupcakesroll"])
async def d10(ctx):
    result = random.randint(1,10)
    await bot.say("From 1-10, you got a...\n[ **"+  str(result)  +"** ]")
    print("d10 called!")

    

#####D20#####
    
@bot.command(pass_context = True, name = "d20")
async def d20(ctx):
    result = random.randint(1,20)
    await bot.say("From 1-20, you got a...\n[ **"+  str(result)  +"** ]")
    if result == 1:
        await bot.say("*Somewhere, an anvil falls on an Umbreon...*")
        print("They found the Umbreon easter egg!")
    print("d20 called!")



#####D30#####
    
@bot.command(pass_context = True, name = "d30")
async def d30(ctx):
    result = random.randint(1,30)
    await bot.say("From 1-30, you got a...\n[ **"+  str(result)  +"** ]")
    print("d30 called!")


#####D50#####
    
@bot.command(pass_context = True, name = "d50")
async def d50(ctx):
    result = random.randint(1,50)
    await bot.say("From 1-50, you got a...\n[ **"+  str(result)  +"** ]")
    print("d50 called!")






######################################################
######################  WHEELS  ######################
######################################################

@bot.command(pass_context = True, name = "chance", aliases = ["chancespace","chancecard","drawchance"])
async def chance(ctx):
    result = random.choice(chanceList)
    await bot.upload("chance/"+result)
    print("Chance called!")

@bot.command(pass_context = True)
async def capsule(ctx):
    result = random.choice(capsuleList)
    await bot.say("You opened the capsule, and found...\n[ **"+  str(result) +"** ]")
    print("Capsule called!")
    
@bot.command(pass_context = True, name = "torracat", aliases = ["torra","torraspace","torracatspace"])
async def torracat(ctx):
    result = random.choice(torracatList)
    await bot.say("Torracat decrees that the following shall happen!\n[ **"+  str(result)  +"** ]")
    print("Torracat called!")
    
@bot.command(pass_context = True, name = "mining", aliases = ["mine","excavate","excavation","minespace","miningspace","excavationspace"])
async def mining(ctx):
    result = random.choice(miningList)
    await bot.say("After some digging, you found...\n[ **"+  str(result)  +"** ]")
    print("Mining called!")

   
    
@bot.command(pass_context = True, name = "bonus1", aliases = ["spaceaward","spacesbonus","spacesaward","spacebonus","award1"])
async def bonus1(ctx):
    result = random.choice(spacebonusList )
    await bot.say("The first award is...\n[ **"+  str(result)  +"** ]")
    print("bonus1 called!") 
    
@bot.command(pass_context = True, name = "bonus2", aliases = ["miscaward","miscbonus","otheraward","otherbonus","award2"])
async def bonus2(ctx):
    result = random.choice(otherbonusList )
    await bot.say("The second award is...\n[ **"+  str(result)  +"** ]")
    print("bonus2 called!")        
    
@bot.command(pass_context = True, name = "bonus3", aliases = ["flataward","flatsbonus","flatsaward","flatbonus","award3"])
async def bonus3(ctx):
    result = random.choice(flatbonusList)
    await bot.say("The third award is...\n[ **"+  str(result)  +"** ]")
    print("bonus3 called!")     
    
    




######################################################
####################  UTILITIES  #####################
######################################################
    
    
@bot.command(pass_context = True, name = "torrashuffle", aliases = ["torracatshuffle","shuffleposition","shufflepositions","positionshuffle"])    
async def torrashuffle(ctx,*args):
    if len(args) > 0:
        listOrig = list(args)
        listShuffled = listOrig.copy()
        random.shuffle(listShuffled)
    else:
        listOrig = ["Player 1","Player 2","Player 3","Player 4"]
        listShuffled = listOrig.copy()
        random.shuffle(listShuffled)
    
    listMoved = [] #Keeping a list of which players have already moved isn't the most efficient way to do this, but...
                   #Most situations should only have an N of 8 or fewer.
                   #Proposal: the shuffled list is actually just a list of indices which can be linked back to the original names.
    sambaSpeech = ""
    for i in range(len(listOrig)):
        if listOrig[i] == listShuffled[i]:
            sambaSpeech += listOrig[i] + " doesn't move!\n"
        else:
            sambaSpeech += listOrig[i] + " moves to " + listShuffled[i] + "'s "
            if listShuffled[i] in listMoved:
                sambaSpeech += "original position!\n"
            else:
                sambaSpeech += "position!\n"
            listMoved.append(listOrig[i])
        
    await bot.say(sambaSpeech)
    

    
@bot.command(pass_context = True, name = "itemshuffle", aliases = ["shuffleitem","shuffleitems"])    
async def itemshuffle(ctx,*args):
    if len(args) > 0:
        listOrig = list(args)
        listShuffled = listOrig.copy()
        random.shuffle(listShuffled)
    else:
        listOrig = ["Player 1","Player 2","Player 3","Player 4"]
        listShuffled = listOrig.copy()
        random.shuffle(listShuffled)
    
    listMoved = [] #Keeping a list of which players have already moved isn't the most efficient way to do this, but...
                   #Most situations should only have an N of 8 or fewer.
                   #Proposal: the shuffled list is actually just a list of indices which can be linked back to the original names.
    sambaSpeech = ""
    for i in range(len(listOrig)):
        if listOrig[i] == listShuffled[i]:
            sambaSpeech += listOrig[i] + ", you can keep your item.\n"
        else:
            sambaSpeech += listOrig[i] + ", give your item to " + listShuffled[i] + "!\n"
        
    await bot.say(sambaSpeech)
    
    
    
@bot.command(pass_context = True, name = "torracatrevolution", aliases = ["torrarevolution","torrarev","torracatrev","revolution","communism","torracommunism","torracatcommunism"])
async def torracatrevolution(ctx,*args):
    try:
        if len(args) > 0:
            sum = 0
            for num in args:
                sum += int(num)
            sum //= len(args)
            await bot.say("Everyone now has " + str(sum) + " coins!")
        else:
            await bot.say("Please specify everyone's total number of coins!\nUsage example: **.torracatrevolution 10 20 15 20**")
    except ValueError:
        await bot.say(num+" isn't a valid number of coins!\nUsage example: **.torracatrevolution 10 20 15 20**")
                
                
######################################################
####################  MAP EVENTS  ####################
######################################################              
                
##### Shifting Sand Land #####
    
@bot.command(pass_context = True, name = "thwomp", aliases = ["thwomps","sslthwomp","sslthwomps"])
async def thwomp(ctx):
    thwompList = ["Blue","Green","Violet"]
    sayString = ""
    for color in thwompList:
        result = random.randint(1,3)
        sayString += color+" Thwomp: **"+str(result)+"**\n"
    await bot.say(sayString)
    print("Thwomp called!")
    
@bot.command(pass_context = True, name = "sslblock", aliases = ["sslcoinblock"])
async def sslblock(ctx):
    result = random.randint(5,30)
    await bot.say("You bashed the block, and out fell...\n[ **"+  str(result)  +" coins!** ]")
    print("sslblock called!")
    
    
    
    
##### Super Training Stadium #####

@bot.command(pass_context = True, name = "machoketoss", aliases = ["machokes","machoke","machokethrow"])
async def machoketoss(ctx):
    initlisty = ["lower left","lower right","upper right","upper left"]
    initindices = [0,1,2,3]
    random.shuffle(initindices)
    sambaSpeech = "The Machoke balled you up and threw you to the **" + initlisty[initindices[0]] + "** corner's ? Space!\n"
    sambaSpeech += "*(If you're already there, go to the " + initlisty[initindices[1]] + " space instead.)*"
    await bot.say(sambaSpeech)
    print("machoketoss called!")
    
@bot.command(pass_context = True, name = "sportsball", aliases = ["stsballs","stsball","sportsballs","stadiumball","stadiumballs","sportball","sportballs"])
async def sportsball(ctx):
    if random.randint(0,1) == 0:
        await bot.say("An Electrode rolls up to you and explodes! You lose 20 coins!")
    else:
        await bot.say("A Golem Ball comes and rolls over you! You'll stay flattened, unable to move for a turn.")
    print("sportsball called!")    
    
##### Luigi's Mansion #####

@bot.command(pass_context = True, name = "boocoins", aliases = ["boocoinsteal"])
async def boocoins(ctx):
    #5% chance of 1
    #20% chance of 5
    #45% chance of 10
    #20% chance of 15
    #10% chance of 20
    cointable = [1,5,5,5,5,10,10,10,10,10,10,10,10,10,15,15,15,15,20,20]
    result = random.choice(cointable)
    if result == 1:
        await bot.say("Boo stole "+ str(result) + " coin!")
    else:
        await bot.say("Boo stole "+ str(result) + " coins!")
    print("boocoins called!")
    
##### Malie Garden #####    

@bot.command(pass_context = True, name = "randomitem", aliases = ["itemwheel","item"])
async def randomitem(ctx):
    result = random.choice(randomitemList)
    await bot.say("Your item is...\n[ **"+  str(result)  +"** ]")
    print("randomitem called!")   
    
@bot.command(pass_context = True, name = "maliewater", aliases = ["water","maliepond","narrowpath","malienarrowpath"])
async def maliewater(ctx):
    result = random.randint(1,20)
    if result <= 8:   
        await bot.say("A Feebas flies out of the water and splashes around! Nothing happens.")
    elif result <= 12:
        await bot.say("Corsola excitedly flies out of the water and lands on you!\n**You've been half-flattened!** Your next turn's roll will be a half roll, and you can't use items.")
    elif result <= 16:
        await bot.say("Octillery pops out of the water. Unhappy to see you, they blast you with an Octazooka.\n**You're blasted back to Start!** You won't get any of the benefits from reaching Start.")
    elif result <= 19:
        await bot.say("Milotic pops out of the water. Glad to have a visitor, they give you a small gift.\n**You got 10 coins!**")
    else:
        await bot.say("Manaphy flies out of the water, looking overjoyed! In their good mood, they're happy to give you a very nice gift!\n**You got a Star!**")        
    print("maliewater called!")
    
@bot.command(pass_context = True, name = "meowth", aliases = ["meowthgamble","maliemeowth","maliegamble","maliecoinflip","meowthcoinflip","meowthflip","malieflip"])
async def meowth(ctx):
    if random.randint(0,1) == 0:
        await bot.say("The coin has been flipped. It comes up...\n**Heads!** Did you win?")
    else:
        await bot.say("The coin has been flipped. It comes up...\n**Tails!** Did you win?")
    print("meowth called!")
    
@bot.command(pass_context = True, name = "maliestar", aliases = ["maliestarspace","maliegardenstar"])
async def maliestar(ctx):
    result = random.randint(0,6)
    while result == prevStarLoc[0]:
        result = random.randint(0,6)
    prevStarLoc[0] = result
    
    imagey = malieStarList[result]
    await bot.say("The Star is now in location " + imagey[-5] + "!")
    await bot.upload("maliestar/"+imagey)
    print("Maliestar called!")    
                
######################################################
######################  EVENTS  ######################
######################################################

#@bot.command(pass_context = True)
#async def freegift(ctx):
#    if ctx.message.channel.id != "373259889826332673":
#        await bot.say("Please call .freegift in the Trading channel!")
#    else:
#        idList = []
#        listFromFile("freegift_ids.txt",idList)
#        if str(ctx.message.author.id) in idList:
#            await bot.say("You already got your free coupon! I only have so many to go around...")
#        else:
#            ticketList = []
#            listFromFile("freegift.txt",ticketList)
#            ticket = random.choice(ticketList)
#            await bot.say(
#ctx.message.author.name + """, your free coupon is...
#the """+ticket+""" Coupon!
#Keep this in your items - you can redeem it to play with """+ticket+"""!
#Or you can trade it with someone else!""")
#            with open("freegift_ids.txt","a") as outFile:
#                print(str(ctx.message.author.id),file=outFile)
#    print("Freegift called!")

@bot.command(pass_context = True)
async def freegift(ctx):
     await bot.say("Sorry, bud, that ship has sailed... There are no more free gift coupons left.\nBut maybe I'll have something else for you later?")


######################################################
###################### ME ONLY  ######################
######################################################

##@bot.command(pass_context = True)
##async def generalhanasu(ctx):
##    #bot says something in general chat.
##    result = random.choice(chanceList)
##    await bot.upload("chance/"+result)
##    print("Chance called!")    

@bot.command(pass_context = True)
async def itsamenammio(ctx):
    if ctx.message.author.id == "161982345207873536":
        await bot.say("Hey, it is you!")
    else:
        await bot.say("No you're not, silly!")

@bot.command(pass_context = True)
async def superTestMessage(ctx):
    if ctx.message.author.id == "161982345207873536":
        await bot.say("Pants!")
    else:
        await bot.say("Are you trying to make me say naughty things? How dare you!")

            

######################################################
######################   MISC   ######################
######################################################
#(for fun, mainly)

@bot.command(pass_context = True, name = "wakeup", aliases = ["areyouthere","areyouhere"])
async def wakeup(ctx):
    await bot.say(":zzz: ...oh... Oh! Ah! I-I'm awake! I'm ready for a party! Always!")
    print("wakeup called!")

@bot.command(pass_context = True)
async def canikickyou(ctx):
    await bot.say("Sure thing! Don't worry, it won't hurt or anything.")
    await bot.say("I hope I can come back for another party, though!")
    print("CanIKickYou called!")

@bot.command(pass_context = True, name = "annoying", aliases = ["youreannoying","shutup","ihateyou"])
async def annoying(ctx):
    await bot.say("Aww, really? Sorry to bother you, then!")
    await bot.say("B-but I'll go teach someone else how to host a party, and bring 'em over!")
    await bot.say("I hope you have a nice day! :heart:")
    print("Annoying called...")

@bot.command(pass_context = True, name = "thanks", aliases = ["thankyou","gracias","arigato","arigatou"])
async def thanks(ctx):
    result = random.choice(thanksList)
    await bot.say(result)
    print("Thanks called!")

@bot.command(pass_context = True, name = "hi", aliases = ["hello","hiya","goodmorning","goodday","goodafternoon","goodevening"])
async def hi(ctx):
    result = random.choice(hiList)
    await bot.say(result)
    print("Hi called!")

@bot.command(pass_context = True)
async def rigged(ctx):
    await bot.say("I am not! :triumph:")
    print("Ping called!")    
    
@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("Pong! ♪")
    print("Ping called!")

bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    await bot.whisper("""Hiiii! I'm Samba, and I'm here to ensure that your party goes smoothly!
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

##WEEKLY_TARGET_CHANNEL = '393628008591917059'
##
##
##
##async def updateWeeklyTask():
##    nextWeeklyTime = 0
##    
##    with open("WeeklyTime.pickle","rb") as infile:
##        nextWeeklyTime = pickle.load(infile)
##
##
##    currDate = datetime.datetime.now()
##
##    
##    if nextWeeklyTime <= currDate:
##
##        weeklyString = ""
##        randomWeekly1 = []
##
##        listFromFile("WeeklyPool.txt",randomWeekly1)
##
##        weeklyString = random.choice(randomWeekly1)
##
##        leftBracket = weeklyString.find('[')
##        
##        if weeklyString.find('[') != -1:
##            rightBracket = weeklyString.find(']')
##            partToReplace = weeklyString[leftBracket:rightBracket+1]
##            partFilename = partToReplace.strip('[]')
##
##            randomWeekly2 = []
##
##            listFromFile("Weekly"+partFilename+".txt",randomWeekly2)
##
##            weeklyString = weeklyString.replace(partToReplace,random.choice(randomWeekly2))
##
##        currWeekly = weeklyString
##
##        with open("WeeklyCurrent.txt","w") as outfile:
##            print(currWeekly,file=outfile)
##
##
##        while nextWeeklyTime <= currDate:
##            nextWeeklyTime += datetime.timedelta(days = 7)
##        
##        with open("WeeklyTime.pickle","wb") as outfile:
##            pickle.dump(nextWeeklyTime,outfile)
##
##        targetChannel = discord.Object(id = WEEKLY_TARGET_CHANNEL);
##
##        await sendWeeklyMessage(targetChannel);
##            
##            
##
##
##async def sendWeeklyMessage(channel):
##
##    with open("WeeklyCurrent.txt","r") as infile:
##        currWeekly = infile.readline().strip()
##
##    with open("WeeklyTime.pickle","rb") as infile:
##        nextWeeklyTime = pickle.load(infile)
##        
##    dateString = nextWeeklyTime.strftime("%B %d!")
##    wholeMessage = "Current task:\n"+currWeekly+"\nFinish by the end of "+str(dateString)
##    await bot.send_message(channel,wholeMessage)
##




##@bot.command(pass_context = True)
##async def weekly(ctx):
##    await sendWeeklyMessage(ctx.message.channel);
    
    

######################################################
#################   BACKGROUND TASK  #################
######################################################
#primarily for weekly reminders

"""
BG_TASK_INTERVAL = 300; #In seconds, how long the background task should sleep.

async def background_task():
    await bot.wait_until_ready()

    while not bot.is_closed:

        #Get runtime, minus microseconds.
        runtime = datetime.datetime.now() - starttime
        runtime -= datetime.timedelta(microseconds = runtime.microseconds)

        await updateWeeklyTask()

        await sleep(BG_TASK_INTERVAL)


bot.loop.create_task(background_task())
"""

bot.run(bot_token)
