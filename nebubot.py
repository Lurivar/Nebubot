#! /usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import datetime
import configparser
import csv
import os

#doc api discord http://discordpy.readthedocs.io/en/latest/api.html


bot = commands.Bot(command_prefix='/', description='h')

#on pars le fichier config pour recup les infos que l'on a besoin pour se connecter
config = configparser.ConfigParser()
config.read('config.ini')
token = config['keys']['discord_nebula']
general_channel_id = config['chan_id']['test']

class Event(object):
    dt = 0
    str = ""
    desc = ""

    def __init__(self, datetime, desc : str):
        self.dt = datetime
        self.str = datetime.strftime("%Hh%M %d/%m/%Y")
        self.desc = desc


async def check_event():
    await bot.wait_until_ready()
    channel = discord.Object(general_channel_id)
    today = datetime.datetime.today()
    margin = datetime.timedelta(days = 3)
    event_tab = []
    for line in open('dates'):
        data = line.split("###")
        date = datetime.datetime.strptime(data[0], '%H:%M %d/%m/%Y')
        desc = data[1].rstrip('\n')
        obj = Event(date, desc)
        if (today <= obj.dt <= today + margin):
            event_tab.append(obj)
    while not bot.is_closed:
        for item in event_tab:
            await bot.send_message(channel, "You have a rendezvous planned at : " + item.str + "\n \"" + item.desc + "\"")
        await bot.send_message(channel, "@everyone, look at this reminder !")
        await asyncio.sleep(86400) # task will run every day - 86400 sec

#toDoDB = []

#def channelDBManager(channel):
#    channelExists = False
#    for db in toDoDB:
#        if db[0] == channel:
#            channelExists = True
#            currentDB = db[1]

#    if not channelExists:
#        toDoDB.append([channel, []])
#        for db in toDoDB:
#            if db[0] == channel:
#                currentDB = db[1]
#    try:
#        return currentDB
#    except:
#        print("channeldbmanager fatal fail - exiting")
#        exit()

#def newToDo(desc, channel):
#    db = channelDBManager(channel)
#    status = True
#    tempTodo = [desc, status]
#    db.append(tempTodo)

#def doneToDo(id, channel):
#    db = channelDBManager(channel)
#    i = 0
#    success = False
#    for todo in db:
#        i += 1
#        if i == id:
#            success = True
#            tempI = i - 1
#            db.remove(db[tempI])
#    return success

#def listToDo(channel):
#    db = channelDBManager(channel)
#    id = 0
#    returnList = []
#    for todo in db:
#        temptodo = []
#        for i in todo:
#            temptodo.append(i)
#        id += 1
#        temptodo.insert(0, id)
#        returnList.append(temptodo)
#    return returnList

#bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#@bot.event

#async def on_message(message):

#    channel = str(message.channel.id)

#    command = str(message.content)

#    if command.startswith("/"):

#        print(toDoDB)

#        if command.startswith("/add "):
#            command = command.replace("/add ", "")
#            if command == "":
#                await bot.send_message(message.channel, ":x: No ToDo entered.")
#                print(":x: No ToDo entered.")
#            newToDo(command, channel)
#            await bot.send_message(message.channel, ":white_check_mark: ToDo `" + command + "` added.")
#            print(":white_check_mark: ToDo '" + command + "' added.")
#        elif command == "/add":
#            await bot.send_message(message.channel, ":x: Usage: `/add [TOD O]`")
#            print(":x: Usage: `/add [TOD O]`")

#        elif command == "/todo":
#            list = listToDo(channel)
#            printline = ""
#            for todo in list:
#                printline = printline + "**[" + str(todo[0]) + "]** - " + str(todo[1]) + "\n"
#            if printline == "":
#                printline = ":metal: **No ToDo's!** :metal:"
#            else:
#                printline = ":pencil: **ToDo's:** :pencil:\n\n" + printline
#            await bot.send_message(message.channel, printline)
#            print(printline)

#        elif command.startswith("/done "):
#            command = command.replace("/done ", "")
#            try:
#                command = int(command)
#            except:
#                await bot.send_message(message.channel, ':x: ID needs to be a number!')
#                print(":x: ID needs to be a number!")
#                return
#            success = doneToDo(command, channel)
#            if success:
#                await bot.send_message(message.channel, ':white_check_mark: ToDo done.')
#                print(":white_check_mark: ToDo deleted")
#            else:
#                await bot.send_message(message.channel, ':x: No ToDo with ID **' + str(command) + '**')
#                print(':x: No ToDo with ID **' + str(command) + '**')
#        elif command == "/done":
#            await bot.send_message(message.channel, ":x: Usage: `/done [ID]`")
#            print(":x: Usage: `/done [ID]`")

#        elif command == "/help":
#            printline = "'/todo' - Show the current todo list.\n'/add [TOD O]' - Add a new todo.\n'/done [ID]' - Mark a todo done (delete).\n'/help' - Show this menu.\nv1.0 by @xdavidhu"
#            printline = ":question: **Help menu:** :question:\n" + "```" + printline + "```"
#            await bot.send_message(message.channel, printline)
#            print(printline)

#        elif command.startswith("/"):
#            printline = ":x: Command `" + command + "` not found. Type `/help` for the help menu."
#            await bot.send_message(message.channel, printline)
#            print(printline)

#@bot.command()
#async def new_rdv(*args):
#    #i = -1
#    d = datetime.datetime.strptime(' '.join(args), '%H:%M %d/%m/%Y')
#    e = Event(d, "No description was given to this event.")
#    num_lines = sum(1 for line in open('dates'))
#    with open('dates', 'a') as file:
#        file.write(str(num_lines) + ": " + e.str + ' *' + e.desc + '*\n')
#    await bot.say("New Rendezvous is set at : " + e.str + "\n \"" + e.desc + "\"")
#    file.close()

@bot.command()
async def new_rdv(*args):
    seq = (args[0], args[1])
    line_count = sum(1 for line in open('dates.csv'))
    try:
        d = (datetime.datetime.strptime(' '.join(seq), '%H:%M %d/%m/%Y'))
        with open('dates.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            if len(args)>2:
                spamwriter.writerow([str(line_count)] + [d.strftime("%Hh%M %d/%m/%Y")] + [args[2]])
            else:
                spamwriter.writerow([str(line_count)] + [d.strftime("%Hh%M %d/%m/%Y")] + ["No description was given for this Rendezvous"])
        csvfile.close()
    except ValueError:
        await bot.say("Error: The date format you entered is invalid\n")

@bot.command()
async def check_rdv():
    with open('dates.csv', 'r') as liste_rdv, open('temp.txt', 'a') as tempf:
        liste_csv = csv.reader(liste_rdv)
        for row in liste_csv:
            tempf.write("ID: " + row[0] + " | Date: " + row[1] + " | Description: " + row[2] + "\n")
    tempf.close()
    with open('temp.txt', 'r') as tempf:
        await bot.say(tempf.read())
    os.remove('temp.txt')
    liste_rdv.close()

@bot.command()
async def del_rdv(*args):
    line_nbr = int(args[0])
    max_line = sum(1 for line in open('dates.csv'))
    await bot.say("Deleting Rendezvous number " + args[0] + "\n...\n")
    if line_nbr >= max_line:
        await bot.say("There is no Rendezvous with this ID. Use /check_rdv to see the list of Rendezvous and their ID\n")
        return
    with open("dates.csv", "r") as inp, open ("new.csv", "w", newline='') as out:
        old_csv = csv.reader(inp)
        new_csv = csv.writer(out)

        line_list = list(old_csv)
        del line_list[line_nbr]
        x = 0
        while x < (max_line - 1):
            line_list[x][0] = str(x)
            x = x + 1
        new_csv.writerows(line_list)
    os.remove('dates.csv')
    os.rename('new.csv' ,'dates.csv')
    inp.close()
    out.close()
    await bot.say("Done !\n")


@bot.command()
async def help_rdv():
    await bot.say("Usage :\n"
    "To add a new Rendezvous: /new_rdv H:M d/m/Y\n \"Description of the event\""
    "To delete a Rendezvous: /del_rdv ID\n"
    "To check the list of Rendezvous: /check_rdv\n"
    "To see this list of commands: /help_rdv")


bot.loop.create_task(check_event())
bot.run(token)
