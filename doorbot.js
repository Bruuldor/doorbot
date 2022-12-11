const moment = require('moment');
const { Client, Intents, Message } = require('discord.js')
const client = new Client({
     intents: 8,
});

client.on("ready", () => {
  console.log("The bot is ready!");
});

const events = {};



client.login('your-bot-token-here');
