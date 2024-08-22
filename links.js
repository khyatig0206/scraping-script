const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');
const fs = require('fs');  // Import the fs module

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/scrape', async (req, res) => {
    const { url } = req.body;

    try {
        const response = await axios.get(url);
        const html = response.data;
        const $ = cheerio.load(html);

        // Extracting data from the page
        let doctors = [];

        $('.resultbox_info').each((index, element) => {
            const href = $(element).find('.resultbox_title_anchorbox').attr('href');
            doctors.push({ href });
        });

        // Convert the array of objects into CSV format
        const csvContent = doctors.map((doctor) => `https://www.justdial.com${doctor.href}`).join('\n');

        // Append the CSV content to an existing file or create the file if it doesn't exist
        fs.appendFileSync('doctors.csv', csvContent + '\n');

        res.json({ message: 'Data scraped and appended to doctors.csv' });
    } catch (error) {
        console.error('Failed to scrape data:', error);
        res.status(500).json({ error: 'Failed to scrape data' });
    }
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
