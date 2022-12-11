import discord
import asyncio

from datetime import datetime, timedelta

client = discord.Client(intents=discord.Intents.all())

# Dictionary to store events, where the key is the event name and the value is a tuple
# containing the event date and a list of users who have signed up for the event
events = {}

@client.event
async def on_ready():
    # Print a message when the bot is ready
    print("Bot is ready!")

    # Check the events dictionary every minute to see if any events are starting soon
    while True:
        # Get the current date and time
        now = datetime.now()

        # Check each event in the events dictionary
        for event_name, event_details in events.items():
            # Get the event date and list of users who have signed up for the event
            event_date, users = event_details
            # Check if the event date is within the next hour
            if event_date > now and event_date < now + timedelta(hours=1):
                # Send a private message to each user who has signed up for the event
                for user in users:
                    await user.send(f"Event '{event_name}' is starting soon on {event_date}")

        # Sleep for 1 minute before checking the events dictionary again
        await asyncio.sleep(60)
                
# Create a new message with the event information
                event_message = await message.channel.send(f"Event '{event_name}' on {event_date}")
                # Add the event to the events dictionary using the message ID as the key
                events[event_message.id] = (event_date, [])

                # Add the reaction to the event message
                await event_message.add_reaction("\U0001F44D")

                # Check if the message starts with the "!remove" command
                if message.content.startswith("!remove"):
                    # Split the message into command and event name
                    command, event_name = message.content.split()
                    # Check if the event name is not empty
                    if event_name:
                        # Check if the event exists in the events dictionary
                        if event_name in events:
                            # Get the event details from the events dictionary
                            event_date, users = events[event_name]

                            # Remove the event from the events dictionary
                            events.pop(event_name)

                            # Send a message to confirm that the event was removed
                            await message.channel.send(f"Event '{event_name}' has been removed.")

                # Check if the message starts with the "!show" command
                elif message.content.startswith("!show"):
                    # Check if the events dictionary is not empty
                    if events:
                        # Iterate over the events in the events dictionary
                        for event_name, (event_date, event_users, event_description) in events.items():
                            # Send a message with the event information
                            await message.channel.send(f"Event '{event_name}' on {event_date}")
                    else:
                        # Send a message to inform the user that there are no events
                        await message.channel.send("There are no events.")        
                        
                        
@client.event
async def on_raw_reaction_add(event):
    # Check if the message ID is in the events dictionary
    if event.message_id in events:
        # Get the event details from the events dictionary
        event_date, users = events[event.message_id]

        # Check if the user who added the reaction is not already in the list of users
        if event.user_id not in users:
            # Get the user object from the event object
            user = event.member

            # Add the user to the list of users who have signed up for the event
            users.append(user)

            # Send a private message to the user to confirm that they signed up for the event
            await user.send(f"You have signed up for event '{event_name}' on {event_date}")

@client.event
async def on_raw_reaction_remove(event):
    # Check if the message ID is in the events dictionary
    if event.message_id in events:
        # Get the event details from the events dictionary
        event_date, users = events[event.message_id]

        # Check if the user who removed the reaction is in the list of users
        if event.user_id in users:
            # Get the user object from the event object
            user = event.member

            # Remove the user from the list of users who have signed up for the event
            users.remove(user)

            # Send a private message to the user to confirm that they withdrew from the event
            await user.send(f"You have withdrawn from event '{event_name}' on {event_date}")
                        
# Run the bot using your Discord bot token
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
client.run(config['discord']['token'])
