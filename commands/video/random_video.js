const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

const { getVideoData } = require('../../robobert/pkg');

module.exports = {
data: new SlashCommandBuilder()
	.setName('video')
	.setDescription('Replies With A Random Video!')
    .addStringOption(option => option
        .setName("video_name")
        .setDescription("The name of a video you want")
        .setRequired(false)),
async execute(interaction) {
    let video_name = interaction.options.getString("video_name");
    if (!video_name){ video_name = await getSudoRandomSlug(); } 
    // using the random slug as the comic extension
    const video = await getVideoData(`https://explosm.net/shorts/${video_name}`);
    // reading the important info from the comic
    const videoDetails = video["shortDetails"];
    // sending the embed
	await interaction.editReply({content: `[A Video Found On Explosm.net](https://explosm.net)\n**video** : ${video["slug"]}\n**youtube-link** :https://www.youtube.com/watch?v=${videoDetails["youtubeid"]}`});
},
};

// THIS SHOULD BE THE CODE; HOWEVER, RANDOM SLUG ISNT RANDOM ATM
async function getRandomSlug(){
    const comic = await getVideoData("https://explosm.net");
    return comic["navigation"][0]["randomSlug"];
}
// A sudo random slug filler until random slug is truly random
async function getSudoRandomSlug(){
    const randomCount = 1 + Math.floor(Math.random() * 10);
    const slugOptions = ["nextSlug","previousSlug","randomSlug"];
    let slug = null;
    let video;
    for(let count = 0; count < randomCount; count++){
        video = await getVideoData(`https://explosm.net/shorts/${slug}`);
        slug = video["navigation"][0][slugOptions[Math.floor(Math.random() * 3)]]
    }
    return slug;
}