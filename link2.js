const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/scrape', async (req, res) => {
    const { url } = req.body;

    try {
        // Launch a browser instance
        const browser = await puppeteer.launch({ headless: false });
        const page = await browser.newPage();

        // Go to the provided URL
        await page.goto(url, { waitUntil: 'networkidle2' });

        // Scroll down the page to load more results
        let previousHeight;
        while (true) {
            // Scroll down the page
            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.waitForTimeout(2000); // Wait for 2 seconds

            const currentHeight = await page.evaluate('document.body.scrollHeight');
            if (currentHeight === previousHeight) {
                break; // Exit the loop if no more content is loaded
            }
        }

        // Extract data from the page
        const doctors = await page.evaluate(() => {
            const results = [];
            const elements = document.querySelectorAll('.resultbox_info');
            elements.forEach(element => {
                const href = element.querySelector('.resultbox_title_anchorbox').getAttribute('href');
                results.push(`https://www.justdial.com${href}`);
            });
            return results;
        });

        // Close the browser
        await browser.close();

        // Convert the array of links into CSV format
        const csvContent = doctors.join('\n');

        // Save the CSV to a file
        fs.writeFileSync('doctors.csv', csvContent);

        res.json({ message: 'Data scraped and saved to doctors.csv' });
    } catch (error) {
        console.error('Failed to scrape data:', error);
        res.status(500).json({ error: 'Failed to scrape data' });
    }
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
