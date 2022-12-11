import discord
import asyncio

from datetime import datetime, timedelta

client = discord.Client(intents=discord.Intents.all())

# Dictionary to store events, where the key is the event name and the value is a tuple
# containing the event date and a list of users who have signed up for the event
events = {}

# Define the on_message event handler
@client.event
async def on_message(message):
    # Check if the message is from a user and not from the bot
    if message.author != client.user:
        # Check if the message starts with the "!event" command
        if message.content.startswith("!event"):
            # Split the message into command, event name, and event description
            command, event_name, *event_description = message.content.split()
            # Check if the event name is not empty
            if event_name:
                # Check if the event date is specified
                if event_description:
                    # Parse the event description
                    event_description = " ".join(event_description)

                    # Check if the event description is not longer than 280 characters
                    if len(event_description) <= 280:
                        # Set the event date and time to the current date and time if not specified
                        event_date = datetime.now()

                        # Check if the event date is in the correct format
                        try:
                            # Parse the event date using the datetime.strptime() method
                            event_date = datetime.strptime(" ".join(event_description), "%Y-%m-%d %H:%M")
                        except ValueError:
                            # Send a message to inform the user of the correct date format
                            await message.channel.send(
                                "Please provide the event date and time in the following format: YYYY-MM-DD HH:MM"
                            )
                            # Return to avoid creating the event
                            return

                        # Create a new message with the event information
                        event_message = await message.channel.send(
                            f"Event '{event_name}' on {event_date}\n{event_description}"
                        )
                        # Add the event to the events dictionary
                        events[event_name] = (event_date, [], event_description)

                        # Add the reaction to the event message
                        await event_message.add_reaction("\U0001F44D")

                        # Send a private message to the user who created the event
                        await message.author.send(
                            f"You have successfully created the event '{event_name}' on {event_date}"
                        )

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
                    event_date = datetime.strptime(" ".join(event_date), "%d-%m-%Y %H:%M")
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
                            
               
                # Check if the message starts with the "!show" command
                        elif message.content.startswith("!show"):
                            # Check if the events dictionary is not empty
                            if events:
                                # Iterate over the events in the events dictionary
                                for event_name, (event_date, event_users, event_description) in events.items():
                                    # Send a message with the event information
                                    await message.channel.send(
                                        f"Event '{event_name}' on {event_date}\n{event_description}"
                                    )
                            else:
                                # Send a message to inform the user that there are no events
                                await message.channel.send("There are no events.")            
# Run the bot using your Discord bot token
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
client.run(config['discord']['token'])
