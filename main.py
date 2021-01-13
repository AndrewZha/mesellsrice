import discord
import random
import calendar
import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import date, datetime
# Scheduler stuff
from apscheduler.schedulers.asyncio import AsyncIOScheduler
sched = AsyncIOScheduler()
sched.configure()
sched.start()

client = discord.Client()
url = "https://markets.businessinsider.com/commodities/rice-price"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")
rice = soup.find("span", {"class": "price-section__current-value"})
daily_rice_stock = rice.text
now = datetime.now()
currentDay = calendar.day_name[date.today().weekday()]
currentTime = now.strftime("%H:%M:%S")

TOKEN = '[TOKEN]'

global reminder_one, announcement
botAnnouncement = False
Officerchannel = 747602050707226658
TSAchannel = 747602050535129089
MPchannel = 760600819799425042
CCchannel = 760600950527492116
EBchannel = 732030332718678076
BDchannel = 768537151134367802
AM10 = "10:00"
PM330 = "15:30"
PM230 = "14:30"
PM4 = "16:00"
PM3 = "15:00"
PM430 = "16:30"
TSA_CCrole = "<@&751679784756707348>"
TSA_Officerrole = "<@&749025182139547679>"
TSA_MProle = "<@&751680164022321155>"
TSA_EDrole = "<@&776637375220285451>"
TSA_EBrole = "<@&751680093696294932>"
TSA_BDrole = "<@&776662542826078208>"
BD_role = "<@&768543627227037697>"

meetingDict = {"Monday": {AM10: [{TSAchannel:TSA_MProle, MPchannel:"@everyone"},
                                 "Just a friendly reminder that there's a Music Production meeting today from 3:30 - 5pm"],
                    PM3:  [{TSAchannel:TSA_MProle, MPchannel:"@everyone"},
                                 "Music Production meeting starts in 30 minutes."],
                    PM330:[{TSAchannel:TSA_MProle, MPchannel:"@everyone"},
                                 "Music Production meeting is starting now"]},

               "Tuesday": {AM10: [{TSAchannel:"@everyone"},
                                  "Just a friendly reminder that there's a TSA meeting today from 3:30 - 4:30pm"],
                    AM10: [{Officerchannel:TSA_Officerrole},
                                  "Just a friendly reminder that there's a staff premeeting today from 3:30 - 4:30pm"],
                    PM230:[{Officerchannel:TSA_Officerrole},
                                  "Staff premeeting starts in 30 minutes"],
                    PM3:  [{Officerchannel:TSA_Officerrole},
                                  "Staff premeeting is starting now."],
                    PM3:  [{TSAchannel:"@everyone"},
                                  "TSA meeting starts in 30 minutes."],
                    PM330:[{TSAchannel:"@everyone"},
                                  "TSA meeting is starting now"]},

               "Wednesday":{AM10: [{TSAchannel:TSA_EDrole},
                                 "Just a friendly reminder that there's an Engineering Design meeting today from 4 - 5pm"],
                    PM330:[{TSAchannel:TSA_EDrole},
                                 "Engineering Design meeting starts in 30 minutes."],
                    PM4  :[{TSAchannel:TSA_EDrole},
                                 "Engineering Design meeting is starting now"]},

               "Thursday": {AM10: [{TSAchannel:TSA_EBrole, EBchannel:"@everyone"},
                                 "Just a friendly reminder that there's an Engineering Brightness meeting today from 3 - 5pm"],
                    PM230:[{TSAchannel:TSA_EBrole, EBchannel:"@everyone"},
                                 "Engineering Brightness meeting starts in 30 minutes."],
                    PM3  :[{TSAchannel:TSA_EBrole, EBchannel:"@everyone"},
                                 "Engineering Brightness meeting is starting now"]},

               "Friday": {AM10: [{TSAchannel:TSA_CCrole, CCchannel:"@everyone"},
                                  "Just a friendly reminder that there's a Coding Crew meeting today from 4 - 6pm"],
                    AM10: [{Officerchannel:TSA_Officerrole},
                                  "Just a friendly reminder that there's a staff meeting today from 3 - 4pm"],
                    PM230:[{Officerchannel:TSA_Officerrole},
                                  "Staff meeting starts in 30 minutes"],
                    PM3:  [{Officerchannel:TSA_Officerrole},
                                  "Staff meeting is starting now."],
                    PM330:[{TSAchannel:TSA_CCrole, CCchannel:"@everyone"},
                                  "Coding Crew meeting starts in 30 minutes."],
                    PM4  :[{TSAchannel:TSA_CCrole, CCchannel:"@everyone"},
                                  "Coding Crew meeting is starting now"]}  }

class MyClient(discord.Client):
    @client.event
    async def on_ready(self):
        '''Self-check'''
        #prints a string statement in the console that lets user know when the bot is active
        print('logged in as {0.user}'.format(client))
        # Adds jobs to scheduler
        for day in meetingDict:
            for time in meetingDict[day]:
                jobDetails = meetingDict[day][time]
                time = time.split(':')
                for dest in jobDetails[0]: #dest : destination
                    role = jobDetails[0][dest]
                    sched.add_job(
                        lambda: self.reminder_ping(dest, role, jobDetails[1]),
                        'cron',
                        day_of_week = day,
                        hour = time[0],
                        minute = time[1]
                        )
                    #print(dest, role, jobDetails[1])

    @client.event
    async def status_task():
        pass

    async def reminder_ping(self, channel, role, message):
        await self.get_channel(channel).send(role + " " + message)

        # Replace this with actual cron scheduling
##        while True:
##            now = datetime.now()                                    ##
##            currentDay = calendar.day_name[date.today().weekday()]  ## SAVE
##            currentTime = now.strftime("%H:%M:%S")                  ##

    async def on_message(self, message):
    #Commands starting with "*"
        cmdStarter = '*'
        msg = message.content
        if msg.startswith(cmdStarter):
            msg = msg[1:]

            '''help command'''
            if msg.split()[0] == 'help':
                embed=discord.Embed(title="Help", description="List of commands that start with *", color=0xd84b4b)
                embed.add_field(name="*help", value="this command", inline=False)
                embed.add_field(name="*rice", value="checks the current price of rice", inline=False)
                await message.channel.send(embed=embed)

            '''checks the price of rice'''
            if msg.split()[0] == 'rice':
                await message.channel.send("Today's rice is $" + str(daily_rice_stock) + " per CWT.")

          
client = MyClient()
client.run(TOKEN)
