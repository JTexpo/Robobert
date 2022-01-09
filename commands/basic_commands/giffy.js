const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

const { TEMPLATES } = require('../../assets/giffy/template.json');

module.exports = {
data: new SlashCommandBuilder()
	.setName('giffy')
	.setDescription('Replies With A Fun Gif!')
    .addStringOption(option => option
        .setName("gif")
        .setDescription("Displays A Gif With Your Text")
        .setChoices([
            ["Fight","FIGHT"],
            ["Hug","HUG"],
            ["Kick","KICK"],
            ["Shush","SHUSH"],
            ["Sip","SIP"],
            ["Speak","SPEAK"]
        ])
        .setRequired(true))
    .addStringOption(option => option
        .setName("text")
        .setDescription("Anythiing In Addition You Want TO Add To THe Gif")
        .setRequired(false)),
async execute(interaction) {
    const gif = interaction.options.getString("gif");
    const text = interaction.options.getString("text");   
    let giffyEmbed = new MessageEmbed()
        .setTitle(TEMPLATES[gif]["CONTENT"])
        .setImage(`attachment://${TEMPLATES[gif]["IMG"]}`)
        .setThumbnail(interaction.member.displayAvatarURL())
        .setColor("RANDOM")
        .setFooter({text: "Try This Command Out For Yourself With /giffy"});
    if (text){ giffyEmbed.setDescription(`"${text}"\n~${interaction.member.displayName}`) }
    else { giffyEmbed.setDescription(`~${interaction.member.displayName}`) }

    return interaction.editReply({
        embeds:[giffyEmbed],
        files: [{
            attachment:`assets/giffy/${TEMPLATES[gif]["IMG"]}`,
            name:TEMPLATES[gif]["IMG"]
          }]
    });
},
};