const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

const axios = require('axios'); 
const fs = require('fs');
const sharp = require('sharp');
sharp.cache(false);

module.exports = {
data: new SlashCommandBuilder()
	.setName('random_comic_generator')
	.setDescription('Replies With A Random Generated Comic!')
    /*
    WORK IN PROGRESS UNKNOWN SOLUTION 
    ---------------------------------
    .addStringOption(option => option
        .setName("extension")
        .setDescription("The 9 letter string extension for rgc")
        .setRequired(false))
    */,
async execute(interaction) {
    let comicId = ""
    rcgTemplate = await getRCGTemplate();
    console.log(rcgTemplate);
    for (const panel of rcgTemplate["panels"]){
        await downloadImage(`https://rcg-cdn.explosm.net/panels/${panel["filename"]}`,`assets/rcg/panel_${panel["column"]}.png`);
        comicId += panel["slug"];
    }

    await sharp('assets/rcg/panel.png')
       .composite([{input:'assets/rcg/panel_1.png', gravity: 'northwest' }])
       .toFile('assets/rcg/panel_build_1.png');
    await sharp('assets/rcg/panel_build_1.png')
       .composite([{input:'assets/rcg/panel_2.png', gravity: 'north' }])
       .toFile('assets/rcg/panel_build_2.png');
    await sharp('assets/rcg/panel_build_2.png')
       .composite([{input:'assets/rcg/panel_3.png', gravity: 'northeast' }])
       .toFile('assets/rcg/panel_build_3.png');
    await sharp('assets/rcg/panel_build_3.png')
       .composite([{input:'assets/rcg/copyright.png', gravity: 'south' }])
       .toFile('assets/rcg/panel_done.png');

    const rcgEmbed = new MessageEmbed()
        .setTitle("A Randomly Generated Comic")
        .setImage("attachment://panel_done.png")
        .setThumbnail(interaction.member.displayAvatarURL())
        .setFields([
            {inline: true, name: "Comic", value: `${comicId}`},
            {inline: true, name: "Author", value: `${interaction.member.displayName}`}
        ])
        .setURL(`https://explosm.net/rcg/${comicId}`)
        .setColor("RANDOM");
    
    await interaction.editReply({
        embeds:[rcgEmbed],
        files: [{
            attachment:'assets/rcg/panel_done.png',
            name:'panel_done.png'
          }]
    });

},
};

async function getRCGTemplate(){
    let template = {};
    await axios.get("https://explosm.net/api/get-random-panels").then((response) => { template = response.data; });
    return template;
}

async function downloadImage(url, filepath) {
    const response = await axios({
        url,
        method: 'GET',
        responseType: 'stream'
    });
    return new Promise((resolve, reject) => {
        response.data.pipe(fs.createWriteStream(filepath))
            .on('error', reject)
            .once('close', () => resolve(filepath)); 
    });
}