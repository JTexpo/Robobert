// Require the necessary discord.js classes
const { Client, Collection, Intents, MessageEmbed } = require('discord.js');
const { INTERVAL_TIME, ANOUNCE_CHANNEL, GUILD} = require('./config.json')
const { getComicData } = require('./robobert/pkg')
const dotenv = require("dotenv");
dotenv.config();

// Create a new client instance
const client = new Client({ intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MESSAGES
] });
client.commands = new Collection();

// LOADING ALL OF THE COMMANDS
const fs = require('fs');
const commandsPath = [
    "basic_commands",
    "comic",
    "video"
];
for (const path  of commandsPath) {
    const commandCollection = fs.readdirSync(`./commands/${path}`).filter(file => file.endsWith('.js'));
    for(const file of commandCollection){
        const command = require(`./commands/${path}/${file}`);
        client.commands.set(command.data.name, command);
    }
}

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
    comicCheck()
});
// ON A COMMAND CREATED
client.on('interactionCreate', async interaction => {
    // IF INTERACTION IS NOT A COMMAND TO RETURN
	if (!interaction.isCommand()) return;
    // IF AN INTERACTION IS NOT INSIDE OF A GUILD
    if (!interaction.inGuild()) return;
    // GRABBING THE COMMAND
	const command = client.commands.get(interaction.commandName);
    // IF NO COMMAND EXISTS OR HAS BEEN LOADED
	if (!command) return;
	try {
        // LOGGING THE COMMAND INTO THE TESTING SERVER FOR DEBUGING PURPOSES
        //logCommand(interaction);
        // HOLDING THE INTERACTION FOR 15 MINUETS
        await interaction.deferReply({ ephemeral: false });
        // EXECUTING THE COMMAND
		await command.execute(interaction);
	} catch (error) {
        try{ 
            // LOGGING THE ERROR
            //logError(interaction,error) 
            // REPLYING BACK TO THE USER THAT SOMETHING WENT WROTN
        }catch{};
		console.log(error);
	}
});

async function comicCheck(){
    const CHGuild = await client.guilds.fetch(GUILD);
    const announceChnl = await CHGuild.channels.fetch(ANOUNCE_CHANNEL);
    let recentComic = "";
    setInterval(async ()=>{try{
        const comic = await getComicData(`https://explosm.net/comics/latest`);
        if (recentComic != comic["slug"]){
            recentComic = comic["slug"];
            const comicDetails = comic["comicDetails"];
            const authorDetails = comicDetails["author"]["authorDetails"];
            // building out the embed
            let comicEmbed = new MessageEmbed()
                .setTitle(`A Comic Found On Explosm.net`)
                .setThumbnail(authorDetails["image"]["mediaItemUrl"])
                .setColor('RANDOM')
                .setURL("https://explosm.net")
                .setFooter({text:comic["slug"]});
            if (comicDetails["comicimgurl"]){
                comicEmbed.setFields([
                        {inline: true, name: "Comic", value: `${comicDetails["comicimgurl"].split("/")[1].split('.')[0]}`},
                        {inline: true, name: "Author", value: `${authorDetails["name"]}`},
                    ]).setImage(`https://files.explosm.net/comics/${comicDetails["comicimgurl"]}`);
            }else{
                comicEmbed.setFields([
                        {inline: true, name: "Comic", value: `${comicDetails["comicimgstaticbucketurl"]["title"]}`},
                        {inline: true, name: "Author", value: `${authorDetails["name"]}`},
                    ]).setImage(`${comicDetails["comicimgstaticbucketurl"]["mediaItemUrl"]}`);
            }
            // sending the embed
            const announceMessage = await announceChnl.send({embeds:[comicEmbed]});
            await announceMessage.crosspost()
    }}catch(err){console.log(err);}},INTERVAL_TIME);
}

// Login to Discord with your client's token
client.login(process.env.DISCORD_TOKEN);