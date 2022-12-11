import discord
from datetime import datetime

client = discord.Client()

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

# Run the bot using your Discord bot token
client.run("YOUR_DISCORD_BOT_TOKEN")
