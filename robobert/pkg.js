const axios = require('axios'); 
const cheerio = require('cheerio'); 

// A Function To Get The Data From A Web Page, WEB SCRAPING
async function getWebData(url,slug){
    // Defining a default comic data
    let web_data = {}
    // Getting the HTML and scrapping for info
    await axios.get(url).then((response) => {
        // loading the html data
        const data_html = cheerio.load(response.data);
        // loading the script data ( bottom of the html, has JSON of everything needed )
        const data_script = JSON.parse(data_html('#__NEXT_DATA__').contents()["0"].data);
        // getting the urqlStates, where the url info lives
        const urqlStates = data_script["props"]["pageProps"]["urqlState"];
        // itterating through the states, because there is not so important info like patron, watermarks, etc.
        for (const [state_id, state_data] of Object.entries(urqlStates)){
            // loading the data, comes as a JSON string
            const data = JSON.parse(state_data["data"]);
            // if the slug exist, return the comic and end the for loop
            if (data[slug]){  web_data = data[slug]; break; }
        }
    });
    // returning the comic data
    return web_data;
}

// Abstracted Function Of getWebData For Comics
async function getComicData(url){
    return getWebData(url,"comic")
}

// Abstracted Function Of getWebData For Videos
async function getVideoData(url){
    return getWebData(url,"short")
}

module.exports = { getComicData, getVideoData };