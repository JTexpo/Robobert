const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
data: new SlashCommandBuilder()
	.setName('dick')
	.setDescription('Creates An Emoji Combo!')
    .addIntegerOption(option => option
        .setName("size")
        .setDescription("How Long You Want The Emoji Combo")
        .setRequired(false)
        .setMinValue(0)
        .setMaxValue(50)),
async execute(interaction) {
    let size = interaction.options.getInteger("size");
    if (!size){ size = Math.floor(Math.random()*10); }
    if (size > 50){ size = 50; }

    let message = "<:dick_4:699753071760113796>";
    const middleEmojis = ["<:dick_3:699753105344167936>","<:dick_2:699753137367547964>"];
    for (let length = 0; length < size; length++){
        message += middleEmojis[Math.floor(Math.random()*2)];
    }
    message += "<:dick_1:699753154815721562>";
    
	await interaction.editReply(message);
},
};