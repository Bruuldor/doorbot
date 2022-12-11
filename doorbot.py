import discord
import asyncio

from datetime import datetime, timedelta

client = discord.Client(intents=discord.Intents.all())

# Dictionary to store events, where the key is the event name and the value is a tuple
# containing the event date and a list of users who have signed up for the event
events = {}

@client.event
async def on_message(message):
    # If the message is from the bot itself, do nothing
    if message.author == client.user:
        return

    # If the message starts with "!event", parse the event details and create the event
    if message.content.startswith("!event"):
        # Split the message into parts, where the first part is the command and the rest is the event details
        parts = message.content.split(" ")
        # Parse the event date from the third part of the message (e.g. "2022-12-11")
        event_date = datetime.strptime(parts[2], "%Y-%m-%d")
        # Create the event using the event name (second part of the message) as the key
        # and the event date and an empty list of users as the value
        events[parts[1]] = (event_date, [])
        # Send a confirmation message to the user who created the event
        await message.channel.send(f"Event '{parts[1]}' created for {event_date}")

    # If the message contains an event name, check if the event exists and sign the user up for it
    # if they react to the message with the "thumbs up" emoji
    for event_name, event_details in events.items():
        if event_name in message.content:
            # Get the event date and list of users who have signed up for the event
            event_date, users = event_details
            # Check if the user has reacted to the message with the "thumbs up" emoji
            if message.reactions[0].emoji == "👍":
                # Add the user to the list of users who have signed up for the event
                users.append(message.author)
                # Update the events dictionary with the updated list of users
                events[event_name] = (event_date, users)
                # Send a confirmation message to the user who signed up for the event
                await message.channel.send(f"{message.author} signed up for '{event_name}' on {event_date}")

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
                
@client.event
async def on_message(message):
    # Check if the message is from a user and not from the bot
    if message.author != client.user:
        # Check if the message starts with the "!event" command
        if message.content.startswith("!event"):
            # Split the message into command and event name
            command, event_name, *event_date = message.content.split()
            # Check if the event name is not empty
            if event_name:
                # Check if the event date is specified
                if event_date:
                    # Parse the event date
                    event_date = datetime.strptime(" ".join(event_date), "%Y-%m-%d %H:%M")
                else:
                    # Set the event date to the current date and time if not specified
                    event_date = datetime.now()

                # Create a new message with the event information
                event_message = await message.channel.send(f"Event '{event_name}' on {event_date}")
                # Add the event to the events dictionary
                events[event_name] = (event_date, [])

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
            
# Run the bot using your Discord bot token
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
client.run(config['discord']['token'])
