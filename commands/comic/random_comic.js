const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

const { getComicData } = require('../../robobert/pkg');

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
    const comicDetails = comic["comicDetails"];
    const authorDetails = comicDetails["author"]["authorDetails"];
    // building out the embed
    let comicEmbed = new MessageEmbed()
        .setTitle(`A Comic Found On Explosm.net`)
        .setThumbnail(authorDetails["image"]["mediaItemUrl"])
        .setColor('RANDOM')
        .setURL("https://explosm.net")
        .setFooter({text:comic_name});

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