#Samba is here to roll dice... and do some other things!

import datetime
import discord
import random
import os
import pickle #Might not be needed, as pickles don't work so well here
import psycopg2
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
byeList = []
riggedList = []
squishtoyList = []
restoreList = []

#Lists of image names, from their respective folders.
chanceList = []
malieStarList = []
boardtestList = []

#Dictionaries matching each image to their respective Samba comment.
chanceDict = {}
malieStarDict = {}

#Used to make a repeated Star location less likely.
#Not guaranteed to work, as bot may restart occasionally.
prevStarLoc = [-1]

#Gets the bot token straight from heroku. You can't see it!
bot_token = os.environ['BOT_TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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

#Helper function
def sqlExecute(sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()

def sqlSelect(sql):
    resultSet = []
    cur = conn.cursor()
    cur.execute(sql)
    try:
        resultSet = cur.fetchall()
    except psycopg2.ProgrammingError:
        print("sqlSelect called, but no result set returned by given sql")
        print("\n"+sql)
    cur.close()
    return resultSet

    







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
    listFromFile("randomTalk/bye.txt",byeList)
    listFromFile("randomTalk/rigged.txt",riggedList)
    listFromFile("randomTalk/squishtoy.txt",squishtoyList)
    listFromFile("randomTalk/restore.txt",restoreList)
    
    listFromFile("randomWheels/randomitem.txt",randomitemList)
    
    listFromFile("randomWheels/spacebonus.txt",spacebonusList)
    listFromFile("randomWheels/otherbonus.txt",otherbonusList)
    listFromFile("randomWheels/flatbonus.txt",flatbonusList)

    for filename in os.listdir("chance"):
        chanceList.append(filename)
    with open("randomWheels/chanceDictionary.txt","r") as infile:
        for line in infile:
            line = line.strip()
            line = line.replace("$%^","\n")
            resultA,resultB = line.split("|")
            if line:
                chanceDict[resultA+".png"] = resultB
        
    for filename in os.listdir("maliestar"):
        malieStarList.append(filename)
    with open("randomWheels/malieStarDictionary.txt","r") as infile:
        for line in infile:
            line = line.strip()
            line = line.replace("$%^","\n")
            resultA,resultB = line.split("|")
            if line:
                malieStarDict[resultA] = resultB

    for filename in os.listdir("boardtest"):
        boardtestList.append(filename)
    
    print("Lists prepared!")

    prevStarLoc = 0

    

    print("Samba is ready!")

    print("Discord.py version:", discord.__version__)














######################################################
################   PLAYER PROFILES   #################
######################################################

#####Get all player rows#####
#  !!Namadu only!!
@bot.command(pass_context = True)
async def namaduEchoPrint(ctx,arg1):
    if ctx.message.author.id == "161982345207873536":
        print (arg1)
    else:
        await bot.say("<:samba:530553475541499914> \"Whoa, whoa, whoa, you're not Namadu! Careful, you could break something!~\"")

@bot.command(pass_context = True)
async def namaduSeeAllPlayerProfileRows(ctx):
    if ctx.message.author.id == "161982345207873536":
        rows = sqlSelect("SELECT * FROM PlayerProfiles;")
        for i in rows:
            print(i);
        await bot.say("<:samba:530553475541499914> \"Go check your logs! Don't let them roll over you!~\"")
    else:
        await bot.say("<:samba:530553475541499914> \"Whoa, whoa, whoa, you're not Namadu! Careful, you could break something!~\"")


#####Initialize Table#####
#  !!Namadu only!!
#@bot.command(pass_context = True)
#async def namaduCreateSambaStatusTable(ctx):
#    if ctx.message.author.id == "161982345207873536":
#        sqlExecute("CREATE TABLE SambaStatus (id varchar PRIMARY KEY, setting varchar);")
#    else:
#        await bot.say("<:samba:530553475541499914> \"Whoa, whoa, whoa, you're not Namadu! Careful, you could break something!~\"")
#####Initialize Table#####
#  !!Namadu only!!
@bot.command(pass_context = True)
async def namaduAddSquishedStatus(ctx):
    if ctx.message.author.id == "161982345207873536":
        sqlExecute("INSERT INTO SambaStatus (id, setting) VALUES ('Squished','No');")
    else:
        await bot.say("<:samba:530553475541499914> \"Whoa, whoa, whoa, you're not Namadu! Careful, you could break something!~\"")

#####Initialize Table#####
#  !!Namadu only!!
#@bot.command(pass_context = True)
#async def namaduCreatePlayerProfileTable(ctx):
#    if ctx.message.author.id == "161982345207873536":
#        sqlExecute("CREATE TABLE PlayerProfiles (id varchar PRIMARY KEY, name varchar, bankedCoins integer, bankedStars integer);")
#    else:
#        await bot.say("<:samba:530553475541499914> \"Whoa, whoa, whoa, you're not Namadu! Careful, you could break something!~\"")


#####New Player#####
@bot.command(pass_context = True, name = "newPlayer")
async def newPlayer(ctx,*args):
    try:
        if len(args)==0:
            await bot.say("<:samba:530553475541499914> \"What's your name, buddy? \nTry like this: .newPlayer Samba the Maractus\"")
            return
        dID = str(ctx.message.author.id)
        
        #Check if player already exists
        if sqlSelect("SELECT id FROM PlayerProfiles WHERE id='"+dID+"';"):
            await bot.say("<:samba:530553475541499914> \"Don't worry, I already have you listed as a player!\"")
        else:
            name = " ".join(args)
            if name.strip("1234567890"):
                await bot.say("<:samba:530553475541499914> \"Hey, I can't give you a name like that! You're more than just a number!\"")
            elif "'" in name or "\\" in name or '"' in name or "<" in name or ">" in name or ":" in name:
                await bot.say("<:samba:530553475541499914> \"Hmm... it looks like I can't any of these characters in your name: \" ' \ < > : \nSorry... Hey, why don't you try a different one?~\"")
            else:
                if sqlSelect("SELECT name FROM PlayerProfiles WHERE name='"+name+"';"):
                    await bot.say("<:samba:530553475541499914> \"Sorry, looks like someone else already has that name. Try a different one!\"")
                else:
                    sqlExecute("INSERT INTO PlayerProfiles (id, name, bankedCoins, bankedStars) VALUES ('"+dID+"','"+name+"',0,0);")
                    await bot.say("<:samba:530553475541499914> \""+name+", you're now registered! Welcome to Pokémon Party!\"")
    except (psycopg2.InternalError, psycopg2.OperationalError) as e:
        await bot.say("<:samba:530553475541499914> \"Whoops, that didn't work... Try again, maybe? Or ask Namadu about it!\"")

#####Change Player Name#####
@bot.command(pass_context = True, name = "changePlayerName")
async def changePlayerName(ctx,*args):
    try:
        dID = str(ctx.message.author.id)
        if not sqlSelect("SELECT id FROM PlayerProfiles WHERE id='"+dID+"';"):
            await bot.say("<:samba:530553475541499914> \"Hmm, I don't have you listed as a player yet...\nTry this: .newPlayer Your Name Here\"")
        else:
            name = " ".join(args)
            if name.strip("1234567890"):
                await bot.say("<:samba:530553475541499914> \"Hey, I can't give you a name like that! You're more than just a number!\"")
            elif "'" in name or "\\" in name or '"' in name or "<" in name or ">" in name or ":" in name:
                await bot.say("<:samba:530553475541499914> \"Hmm... it looks like I can't any of these characters in your name: \" ' \ < > : \nSorry... Hey, why don't you try a different one?~\"")
            else:
            matchingName = sqlSelect("SELECT id, name FROM PlayerProfiles WHERE name='"+name+"';")
                if matchingName:
                    if matchingName[0][0] == dID:
                        await bot.say("<:samba:530553475541499914> \"Okay! Your name has been changed from "+name+" to... uh... "+name+"?\"")
                    else:
                        await bot.say("<:samba:530553475541499914> \"Sorry, looks like someone else already has that name. Try a different one!\"")
                else:
                    sqlExecute("UPDATE PlayerProfiles SET name = '"+name+"' WHERE id = '"+dID+"';")
                    await bot.say("<:samba:530553475541499914> \"Okay! From now on, I'll call you "+name+"!~\"")
    except (psycopg2.InternalError, psycopg2.OperationalError) as e:
        await bot.say("<:samba:530553475541499914> \"Whoops, that didn't work... Try again, maybe? Or ask Namadu about it!\"")
      
        


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
        await bot.say("<:samba:530553475541499914> \"From 1-"+str(num)+", you got a...\"\n[ **"+  str(result)  +"** ]")
    except ValueError:
        await bot.say("<:samba:530553475541499914> \"Uhhhh... looks like I don't have that kind of dice, whoops!\"")
    print("Roll called with " + arg + "!")

#####D6#####

@bot.command(pass_context = True, name = "move", aliases = ["randomroll","d6","6d","curry","curryroll","rollasixsideddiepleasesamba"])
async def move(ctx):
    result = random.randint(1,6)
    await bot.say("<:samba:530553475541499914> \"From 1-6, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("Move called!")

#####2D6#####

@bot.command(pass_context = True, name = "mushroom", aliases = ["mega","mush","megamush","megamushroom","2d6","doubleroll","doublemove"])
async def mushroom(ctx):
    result1 = random.randint(1,6)
    result2 = random.randint(1,6)
    sayString = ""
    sayString += "<:samba:530553475541499914> \"With two dice, you rolled "+str(result1)+" and "+str(result2)+"! The total is...\"\n"
    sayString += "[ **"+  str(result1+result2)  +"** ]\n"
    if result1 == result2:
        sayString += "<:samba:530553475541499914> \"*Hey, you got doubles!*\""
    await bot.say(sayString)
    print("Mushroom called!")


#####D2#####

@bot.command(pass_context = True, name = "d2")
async def d2(ctx):
    result = random.randint(1,2)
    await bot.say("<:samba:530553475541499914> \"From 1-2, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("d2 called!")    
    
#####COINFLIP#####


@bot.command(pass_context = True, name = "coinflip", aliases = ["flipcoin"])
async def coinflip(ctx):
    result = random.choice(("Heads","Tails"))
    await bot.say("<:samba:530553475541499914> \"Flip! It's looking like...\"\n[ **"+  str(result)  +"** ]")
    print("coinflip called!")    
    
#####D3#####

@bot.command(pass_context = True, name = "halfmove", aliases = ["halfroll","half","d3","mini","minimush","minimushroom"])
async def halfmove(ctx):
    result = random.randint(1,3)
    await bot.say("<:samba:530553475541499914> \"From 1-3, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("Halfmove called!")

#####D10#####
    
@bot.command(pass_context = True, name = "d10", aliases = ["grape","grapes","graperoll","grapesroll","cupcake","cupcakes","cupcakeroll","cupcakesroll"])
async def d10(ctx):
    result = random.randint(1,10)
    await bot.say("<:samba:530553475541499914> \"From 1-10, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("d10 called!")

    

#####D20#####
    
@bot.command(pass_context = True, name = "d20")
async def d20(ctx):
    result = random.randint(1,20)
    await bot.say("<:samba:530553475541499914> \"From 1-20, you got a...\"\n[ **"+  str(result)  +"** ]")
    if result == 1:
        await bot.say("*Somewhere, an anvil falls on an Umbreon...*")
        print("They found the Umbreon easter egg!")
    print("d20 called!")



#####D30#####
    
@bot.command(pass_context = True, name = "d30")
async def d30(ctx):
    result = random.randint(1,30)
    await bot.say("<:samba:530553475541499914> \"From 1-30, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("d30 called!")


#####D50#####
    
@bot.command(pass_context = True, name = "d50")
async def d50(ctx):
    result = random.randint(1,50)
    await bot.say("<:samba:530553475541499914> \"From 1-50, you got a...\"\n[ **"+  str(result)  +"** ]")
    print("d50 called!")






######################################################
######################  WHEELS  ######################
######################################################

@bot.command(pass_context = True, name = "chance", aliases = ["chancespace","chancecard","drawchance"])
async def chance(ctx):
    await bot.say("<:samba:530553475541499914> \"Ooooo!~ Chance time!~ Time to take a chance with chance!~ Looks like you got...\"")
    result = random.choice(chanceList)
    #result = "Zukos_Prank_Card.png"  #For testing multiline comments
    comment = chanceDict[result]
    await bot.upload("chance/"+result)
    await bot.say(comment)
    print("Chance called!")

@bot.command(pass_context = True)
async def capsule(ctx):
    result = random.choice(capsuleList)
    resultA,resultB = result.split('|')
    await bot.say("<:samba:530553475541499914> \"OOO!~ A surprise! I wonder what's inside... Time to find out!~\"\n[ **"+  str(resultA) +"** ]\n<:samba:530553475541499914> \""+resultB+"\"")
    print("Capsule called!")
    
@bot.command(pass_context = True, name = "torracat", aliases = ["torra","torraspace","torracatspace"])
async def torracat(ctx):
    result = random.choice(torracatList)
    resultA,resultB = result.split('|')
    resultB = "<:samba:530553475541499914> \"" + resultB + "\""
    if resultA == "Torracat Pity":
        resultB += "\n<:Torracat:370628275795394560> *Does a quick stomp onto Samba as payment for her showing up.*"
    await bot.say("<:samba:530553475541499914> \"Uh oh, looks like this time she wants...\"\n[ **"+  str(resultA)  +"** ]\n"+resultB)
    print("Torracat called!")
    
@bot.command(pass_context = True, name = "mining", aliases = ["mine","excavate","excavation","minespace","miningspace","excavationspace"])
async def mining(ctx):
    result = random.choice(miningList)
    resultA,resultB = result.split('|')
    resultB = "<:samba:530553475541499914> \"" + resultB + "\""
    if resultA == "Razor Claw":
        resultB += "\n<:Zuko:376248129734967296> *Shoves Samba aside.* \"Hey look at that! You got the best item in the game! Grats!\""
    await bot.say("<:samba:530553475541499914> \"Dig!~ Dig!~ Diggy!~ Looks like you dug up...\"\n[ **"+  str(resultA)  +"** ]\n"+resultB)
    print("Mining called!")

   
    
@bot.command(pass_context = True, name = "bonus1", aliases = ["spaceaward","spacesbonus","spacesaward","spacebonus","award1"])
async def bonus1(ctx):
    result = random.choice(spacebonusList )
    result = result.replace("$%^","\n")
    await bot.say("<:samba:530553475541499914> \"It looks like the space related award is...\n**"+  str(result))
    print("bonus1 called!") 
    
@bot.command(pass_context = True, name = "bonus2", aliases = ["miscaward","miscbonus","otheraward","otherbonus","award2"])
async def bonus2(ctx):
    result = random.choice(otherbonusList )
    result = result.replace("$%^","\n")
    await bot.say("<:samba:530553475541499914> \"Seems like the gameplay related award is...\n**"+  str(result))
    print("bonus2 called!")        
    
@bot.command(pass_context = True, name = "bonus3", aliases = ["flataward","flatsbonus","flatsaward","flatbonus","award3"])
async def bonus3(ctx):
    result = random.choice(flatbonusList)
    result = result.replace("$%^","\n")
    await bot.say("<:samba:530553475541499914> \"Wowie, it's looking like the flattening related award is...\n**"+  str(result))
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
    torraSpeech = "<:Torracat:370628275795394560> \"Okay, move it! Everyone swap!"
    for i in range(len(listOrig)):
        torraSpeech += "\n"
        if listOrig[i] == listShuffled[i]:
            torraSpeech += listOrig[i] + " doesn't move!"
        else:
            torraSpeech += listOrig[i] + " moves to " + listShuffled[i] + "'s "
            if listShuffled[i] in listMoved:
                torraSpeech += "original position!"
            else:
                torraSpeech += "position!"
            listMoved.append(listOrig[i])
    torraSpeech += "\""
    await bot.say(torraSpeech)
    

    
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
    torraSpeech = "<:Torracat:370628275795394560> \"Alright, time to do some trading around here!"
    for i in range(len(listOrig)):
        torraSpeech += "\n"
        if listOrig[i] == listShuffled[i]:
            torraSpeech += listOrig[i] + ", you can keep your item."
        else:
            torraSpeech += listOrig[i] + ", give your item to " + listShuffled[i] + "!"
    torraSpeech += "\""
    await bot.say(torraSpeech)
    
    
    
@bot.command(pass_context = True, name = "torracatrevolution", aliases = ["torrarevolution","torrarev","torracatrev","revolution","communism","torracommunism","torracatcommunism"])
async def torracatrevolution(ctx,*args):
    try:
        if len(args) > 0:
            sum = 0
            for num in args:
                sum += int(num)
            sum //= len(args)
            await bot.say("<:Torracat:370628275795394560> \"Everyone now has **" + str(sum) + "** Coins! Deal with it!\"")
        else:
            await bot.say("<:Torracat:370628275795394560> \"Hey, you did it wrong! Do it right this time!\"\nLike this: **.torracatrevolution 10 20 15 20**\"")
    except ValueError:
        await bot.say("<:Torracat:370628275795394560> \"Hey, you did it wrong! Do it right this time!\nLike this: **.torracatrevolution 10 20 15 20**\"")
                
                
######################################################
####################  MAP EVENTS  ####################
######################################################              
                
##### Shifting Sand Land #####
    
@bot.command(pass_context = True, name = "thwomp", aliases = ["thwomps","sslthwomp","sslthwomps"])
async def thwomp(ctx):
    thwompList = ["Blue","Green","Violet"]
    sayString = "<:samba:530553475541499914> \"Thwomps' turn to move!~\"\n"
    for color in thwompList:
        result = random.randint(1,3)
        sayString += color+" Thwomp: **"+str(result)+"**\n"
    await bot.say(sayString)
    print("Thwomp called!")
    
@bot.command(pass_context = True, name = "sslblock", aliases = ["sslcoinblock"])
async def sslblock(ctx):
    result = random.randint(5,30)
    await bot.say("*You bashed the block, and out fell...*\n[ **"+  str(result)  +" coins!** ]\n<:samba:530553475541499914> \"Don't spend it all in one place!~\"")
    print("sslblock called!")
    
    
    
    
##### Super Training Stadium #####

@bot.command(pass_context = True, name = "machoketoss", aliases = ["machokes","machoke","machokethrow"])
async def machoketoss(ctx):
    initlisty = ["lower left","lower right","upper right","upper left"]
    initindices = [0,1,2,3]
    random.shuffle(initindices)
    sambaSpeech = "*The Machoke balled you up and threw you to the* ***" + initlisty[initindices[0]] + "*** *corner's ? Space!*\n"
    sambaSpeech += "*(If you're already there, go to the* ***" + initlisty[initindices[1]] + "*** *space instead.)*\n"
    sambaSpeech += "<:samba:530553475541499914> \"Get on the ball? You ARE the ball!~\""

    await bot.say(sambaSpeech)
    print("machoketoss called!")
    
@bot.command(pass_context = True, name = "sportsball", aliases = ["stsballs","stsball","sportsballs","stadiumball","stadiumballs","sportball","sportballs"])
async def sportsball(ctx):
    if random.randint(0,1) == 0:
        await bot.say("*An Electrode rolls up to you and explodes!* ***You lose 20 coins!***\n<:samba:530553475541499914> \"**BOOM!** That was exciting to watch!~... Though uh, sorry about your coins.\"")
    else:
        await bot.say("*A Golem Ball comes and rolls over you!* ***You'll stay flattened, unable to move for a turn.***\n<:samba:530553475541499914> \"Woah! That looked a bit heavier than a normal ball!\"")
    print("sportsball called!")    
    
##### Luigi's Mansion #####

@bot.command(pass_context = True, name = "boocoins", aliases = ["boocoinsteal","boocoin","boocoinssteal"])
async def boocoins(ctx):
    #5% chance of 1
    #20% chance of 5
    #45% chance of 10
    #20% chance of 15
    #10% chance of 20
    cointable = [1,5,5,5,5,10,10,10,10,10,10,10,10,10,15,15,15,15,20,20]
    result = random.choice(cointable)
    if result == 1:
        await bot.say("Boo stole "+ str(result) + " coin!\n<:samba:530553475541499914> \"Oh dear, I hope this doesn't ruin any friendships!\"")
    else:
        await bot.say("Boo stole "+ str(result) + " coins!\n<:samba:530553475541499914> \"Oh dear, I hope this doesn't ruin any friendships!\"")
    print("boocoins called!")
    
##### Malie Garden #####    

@bot.command(pass_context = True, name = "randomitem", aliases = ["itemwheel","item"])
async def randomitem(ctx):
    result = random.choice(randomitemList)
    resultA,resultB = result.split('|')
    await bot.say("<:samba:530553475541499914> \"Looks like you're ending up with...\"\n[ **"+  str(resultA)  +"** ]\n<:samba:530553475541499914> \""+str(resultB)+"\"")
    print("randomitem called!")   
    
@bot.command(pass_context = True, name = "maliewater", aliases = ["water","maliepond","narrowpath","malienarrowpath"])
async def maliewater(ctx):
    result = random.randint(1,20)
    if result <= 8:   
        await bot.say("*A Feebas flies out of the water and splashes around! Nothing happens.*\n<:samba:530553475541499914> \"Well, at least they tried!~\"")
    elif result <= 12:
        await bot.say("*Corsola excitedly flies out of the water and lands on you!*\n***You've been half-flattened!*** *Your next turn's roll will be a half roll, and you can't use items.*\n<:samba:530553475541499914> \"Oof! Talk about a heavy entrance!\"")
    elif result <= 16:
        await bot.say("*Octillery pops out of the water. Unhappy to see you, they blast you with an Octazooka.*\n***You're blasted back to Start!*** *You won't get any of the benefits from reaching Start.*\n<:samba:530553475541499914> \"Woah! You went flying! Are you okay!?\"")
    elif result <= 19:
        await bot.say("*Milotic pops out of the water. Glad to have a visitor, they give you a small gift.*\n***You got 10 coins!***\n<:samba:530553475541499914> \"Wow!~ What a beautiful and nice Milotic!~\"")
    else:
        await bot.say("*Manaphy flies out of the water, looking overjoyed! In their good mood, they're happy to give you a very nice gift!*\n***You got a Star!***\n<:samba:530553475541499914> \"Wowie!~ What a very nice run in!~ They looked very happy to give you that gift!~\"")        
    print("maliewater called!")
    
@bot.command(pass_context = True, name = "meowth", aliases = ["meowthgamble","maliemeowth","maliegamble","maliecoinflip","meowthcoinflip","meowthflip","malieflip"])
async def meowth(ctx):
    if random.randint(0,1) == 0:
        await bot.say("*The coin has been flipped. It comes up...*\n**Heads!**\n<:samba:530553475541499914> \"Did you win?\"")
    else:
        await bot.say("*The coin has been flipped. It comes up...*\n**Tails!**\n<:samba:530553475541499914> \"Did you win?\"")
    print("meowth called!")
    
@bot.command(pass_context = True, name = "maliestar", aliases = ["maliestarspace","maliegardenstar"])
async def maliestar(ctx):
    result = random.randint(0,6)
    while result == prevStarLoc[0]:
        result = random.randint(0,6) #Inefficient way to avoid repeats, but should work fine.
    prevStarLoc[0] = result
    
    imagey = malieStarList[result]
    comment = malieStarDict[str(result+1)]
    await bot.say(comment)
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

#@bot.command(pass_context = True)
#async def freegift(ctx):
#     await bot.say("Sorry, bud, that ship has sailed... There are no more free gift coupons left.\nBut maybe I'll have something else for you later?")


######################################################
###################### ME ONLY  ######################
######################################################   

##@bot.command(pass_context = True)
##async def itsamenammio(ctx):
##    if ctx.message.author.id == "161982345207873536":
##        await bot.say("Hey, it is you!")
##    else:
##        await bot.say("No you're not, silly!")
##
##@bot.command(pass_context = True)
##async def superTestMessage(ctx):
##    if ctx.message.author.id == "161982345207873536":
##        await bot.say("Pants!")
##    else:
##        await bot.say("Are you trying to make me say naughty things? How dare you!")

            

######################################################
######################   MISC   ######################
######################################################
#(for fun, mainly)

@bot.command(pass_context = True, name = "wakeup", aliases = ["areyouthere","areyouhere"])
async def wakeup(ctx):
    await bot.say("<:samba:530553475541499914> \"Oh! Uh! I wasn't sleeping! Nope! I definitely don't sleep with my eye holes opened!\"")
    print("wakeup called!")

#@bot.command(pass_context = True)
#async def canikickyou(ctx):
#    await bot.say("Sure thing! Don't worry, it won't hurt or anything.")
#    await bot.say("I hope I can come back for another party, though!")
#    print("CanIKickYou called!")

@bot.command(pass_context = True, name = "annoying", aliases = ["youreannoying","shutup"])
async def annoying(ctx):
    await bot.say("<:Zuko:376248129734967296> *Quickly runs by and smacks a strip of duct tape over Samba's mouth!*\n<:samba:530553475541499914> \"MMMMPH!?\"")
    print("Annoying called...")

@bot.command(pass_context = True, name = "bye", aliases = ["farewell","goodbye","later","seeya"])
async def bye(ctx):
    result = random.choice(byeList)
    await bot.say(result)
    print("Bye called!")

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
    result = random.choice(riggedList)
    await bot.say(result)
    print("Rigged called!")    
    
@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("<:samba:530553475541499914> \"Pong!~\"")
    print("Ping called!")

@bot.command(pass_context = True, name = "whoareyou", aliases = ["introduction","intro"])
async def whoareyou(ctx):
    await bot.say("<:samba:530553475541499914> \"Hiya!~ My name is Samba, I'm a Maractus, and I am the new host hired by Epic Umbreon! My other job is hosting and judging fights in a fancy arena for crowds of people for entertainment!~ If you need anything, feel free to let me know! I can do things like commands, helping with games, even being a squish toy if you need to relieve some stress!~\"")
    print("Whoareyou called!")

@bot.command(pass_context = True, name = "squishtoy", aliases = ["squish","squishyou","squashtoy","squash","squashyou","flattentoy","flatten","flattenyou"])
async def squishtoy(ctx):
    if sqlSelect("SELECT id, setting FROM SambaStatus WHERE id = 'Squished'")[0][1] == "Yes":
        await bot.say("*As you go to look for Samba, you accidently step on her as if she was a rug going unnoticed. Looks like someone already flattened her!*")
    else:
        result = random.choice(squishtoyList)
        result = result.replace("$%^","\n")
        await bot.say(result)
        try:
            sqlExecute("UPDATE SambaStatus SET setting = 'Yes' WHERE id = 'Squished';")
        except (psycopg2.InternalError, psycopg2.OperationalError) as e:
            print("But she didn't flatten...")
    print("Squishtoy called!")

@bot.command(pass_context = True, name = "restore", aliases = ["unsquish","unsquishyou","unsquash","unsquashyou","unflatten","unflattenyou"])
async def restore(ctx):
    if sqlSelect("SELECT id, setting FROM SambaStatus WHERE id = 'Squished'")[0][1] == "No":
        await bot.say("*You awkwardly look at Samba as if expecting to do something with her, but she currently isn't in a flattened state.*")
    else:
        result = random.choice(restoreList)
        await bot.say(result)
        try:
            sqlExecute("UPDATE SambaStatus SET setting = 'No' WHERE id = 'Squished';")
        except (psycopg2.InternalError, psycopg2.OperationalError) as e:
            print("But she didn't restore...")
    print("Restore called!")

@bot.command(pass_context = True, name = "boardtest", aliases = ["eventtest","eventest","sambatest"])
async def boardtest(ctx):
    result = random.choice(boardtestList)
    await bot.upload("boardtest/"+result)
    print("Boardtest called!")
    

bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    await bot.say("Looking for help? You can find everything you need at <#370048694332162049>!")
    print("Help called!")


######################################################
###################### ME ONLY  ######################
######################################################

@bot.command(pass_context = True, name = "ventriloquy")
async def ventriloquy(ctx, args):
    if ctx.message.author.id == "161982345207873536":
        #First argument should be channel ID, second argument should be message IN QUOTES.
        #Use those to send that message to that channel.
        pass
    print("Ventriloquy called!")    

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
