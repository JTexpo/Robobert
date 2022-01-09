const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

const { getComicData, buildComicEmbed } = require('../../robobert/pkg');

module.exports = {
data: new SlashCommandBuilder()
	.setName('comic')
	.setDescription('Replies With A Random Comic!')
    .addStringOption(option => option
        .setName("comic_name")
        .setDescription("The name of a comic you want")
        .setRequired(false)),
async execute(interaction) {
    let comic_name = interaction.options.getString("comic_name");
    if (!comic_name){ comic_name = await getSudoRandomSlug(); } 
    // using the random slug as the comic extension
    const comic = await getComicData(`https://explosm.net/comics/${comic_name}`);
    // reading the important info from the comic
    const comicEmbed = buildComicEmbed(comic);
    // sending the embed
	await interaction.editReply({embeds : [comicEmbed]});
},
};
// THIS SHOULD BE THE CODE; HOWEVER, RANDOM SLUG ISNT RANDOM ATM
async function getRandomSlug(){
    const comic = await getComicData("https://explosm.net");
    return comic["navigation"][0]["randomSlug"];
}
// A sudo random slug filler until random slug is truly random
async function getSudoRandomSlug(){
    const randomCount = 1 + Math.floor(Math.random() * 10);
    const slugOptions = ["nextSlug","previousSlug","randomSlug"];
    let slug = null;
    let comic;
    for(let count = 0; count < randomCount; count++){
        comic = await getComicData(`https://explosm.net/comics/${slug}`);
        slug = comic["navigation"][0][slugOptions[Math.floor(Math.random() * 3)]]
    }
    return slug;
}