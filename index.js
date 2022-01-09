// Require the necessary discord.js classes
const { Client, Collection, Intents, MessageEmbed } = require('discord.js');
const { INTERVAL_TIME, ANOUNCE_CHANNEL, GENERAL_CHANNEL, TOPIC_CHANNEL, GUILD, RECENT_COMIC} = require('./config.json')
const { getComicData, buildComicEmbed } = require('./robobert/pkg')
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
    const generalChnl = await CHGuild.channels.fetch(GENERAL_CHANNEL);
    const topicChnl = await CHGuild.channels.fetch(TOPIC_CHANNEL);
    let recentComic = RECENT_COMIC;
    setInterval(async ()=>{try{
        const comic = await getComicData(`https://explosm.net/comics/latest`);
        if (recentComic != comic["slug"]){
            recentComic = comic["slug"];
            const comicEmbed = buildComicEmbed(comic);
            // sending the embed
            const announceMessage = await announceChnl.send({embeds:[comicEmbed]});
            await announceMessage.crosspost()
            const comicThread = await announceMessage.startThread({name: `COMIC ${comic["slug"]}`});
            
            const commentEmbed = new MessageEmbed()
                .setTitle("A New Comic Was Posted")
                .setDescription(`Want To Comment On ${comic["comicDetails"]["author"]["authorDetails"]["name"]}'s Comic?\nCheck Out This Topic Thread <#${comicThread.id}>`)
                .setImage("attachment://checkout.png")
                .setThumbnail(comic["comicDetails"]["author"]["authorDetails"]["image"]["mediaItemUrl"])
                .setColor("RANDOM");

            const commentMessageDetails = {
                embeds:[commentEmbed],
                files: [{
                    attachment:'assets/comicUpdate/checkout.png',
                    name:'checkout.png'
                  }]
            }
            generalChnl.send(commentMessageDetails);
            topicChnl.send(commentMessageDetails);
    }}catch(err){console.log(err);}},INTERVAL_TIME);
}

// Login to Discord with your client's token
client.login(process.env.DISCORD_TOKEN);