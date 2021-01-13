import discord
import random
import calendar
import datetime
import requests
import asyncio
from datetime import date, datetime
# Scheduler stuff
from apscheduler.schedulers.asyncio import AsyncIOScheduler
sched = AsyncIOScheduler()
sched.configure()
sched.start()

client = discord.Client()
now = datetime.now()
currentDay = calendar.day_name[date.today().weekday()]
currentTime = now.strftime("%H:%M:%S")

TOKEN = '[TOKEN]'

global reminder_ping, announcement

meetingDict = {"Tue": {'12:45' : [{"768642751376916484":"<@&768642751247679577>"}, "Hey, this is a test ping"]
                      }
            
               }

class MyClient(discord.Client):
    async def reminder_ping(self, channel, role, message):
        await self.get_channel(channel).send(role + " " + message)

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

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
client = MyClient()
client.run(TOKEN)
