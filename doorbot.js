const Discord = require('discord.js');
const moment = require('moment');
const client = new Discord.Client();

const scheduleEvent = (message, eventDate) => {
  // Parse the event date using moment.js
  const parsedEventDate = moment(eventDate, 'DD-MM-YYYY HH:mm');

  // Check if the parsed date is valid
  if (!parsedEventDate.isValid()) {
    return message.channel.send('Please provide a valid event date in the format %d-%m-%y %H:%M');
  }

  // Check if the provided date is in the future
  if (parsedEventDate.isBefore(moment())) {
    return message.channel.send('Please provide a date in the future.');
  }

  // Save the event in the database
  // The event object should have a title and a date field
  const event = {
    title: message.content,
    date: parsedEventDate
  };
  // Save the event in the database
  saveEvent(event);

  // Add a reaction collector to the message to allow users to sign up for the event
  const filter = (reaction, user) => {
    return user.id !== message.author.id && reaction.emoji.name === '👍';
  };
  message.awaitReactions(filter, { max: 1 }).then(collected => {
    const users = collected.users.array();
    // Send a confirmation message to each user who signed up for the event
    for (const user of users) {
      user.send('You have signed up for the event. We will remind you 24 hours before the event starts.');
    }
  });
};

// This function sends reminders to the users who have signed up for an event
const remindUsers = (event) => {
  // Get the list of users who have signed up for the event from the database
  const users = getEventSignups(event);

  // Calculate the time remaining until the event starts
  const timeRemaining = moment(event.date).diff(moment(), 'hours');

  // If there are 24 hours or less remaining until the event starts, send reminders to the users
  if (timeRemaining <= 24) {
    for (const user of users) {
      user.send('This is a reminder that the event is starting in 24 hours. See you there!');
    }
  }

  // If there is 1 hour or less remaining until the event starts, send reminders to the users
  if (timeRemaining <= 1) {
    for (const user of users) {
      user.send('This is a reminder that the event is starting in 1 hour. See you there!');
    }
  }
};

client.on('message', message => {
  // Check if the message starts with '!schedule'
  if (message.content.startsWith('!schedule')) {
    // Split the message into an array of words
    const words = message.content.split(' ');

    // The event date should be the second word in the message
    const eventDate = words[1];

    // Schedule the event
    scheduleEvent(message, eventDate);
}

// Check if the message is '!remove'
if (message.content === '!remove') {
// Get the event that the user has created from the database
const event = getUserEvent(message.author.id);
    // Check if the user has an event scheduled
if (!event) {
  return message.channel.send('You do not have any events scheduled.');
}

// Remove the event from the database
removeEvent(event);
message.channel.send('The event has been removed.');
}
});

// This function is called every hour to remind the users of upcoming events
setInterval(() => {
// Get all the events from the database
const events = getAllEvents();

// Iterate over each event and send reminders to the users
for (const event of events) {
remindUsers(event);
}
}, 60 * 60 * 1000);

client.login('your-bot-token-here');
