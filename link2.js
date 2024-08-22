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
        const browser = await puppeteer.launch({ headless: false });
        const page = await browser.newPage();

        await page.goto(url, { waitUntil: 'networkidle2', timeout: 120000 });

        // Wait for the necessary elements to load initially
        await page.waitForSelector('.resultbox_info');

        const doctors = new Set();

        let previousHeight;
        while (doctors.size < 100) {  // Adjust the number of unique entries you want to collect
            previousHeight = await page.evaluate('document.body.scrollHeight');
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
            await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 2000)));  // Wait for 2 seconds for the next set of data to load

            // Extract data from the page
            const newDoctors = await page.evaluate(() => {
                const results = [];
                const elements = document.querySelectorAll('.resultbox_info');
                elements.forEach(element => {
                    const anchor = element.querySelector('.resultbox_title_anchorbox');
                    if (anchor) {
                        const href = anchor.getAttribute('href');
                        results.push(`https://www.justdial.com${href}`);
                    }
                });
                return results;
            });

            // Add only unique entries to the doctors set
            newDoctors.forEach(doctor => doctors.add(doctor));

            const currentHeight = await page.evaluate('document.body.scrollHeight');
            if (currentHeight === previousHeight) {
                break;  // Exit loop if no more content is loaded
            }
        }

        await browser.close();

        // Prepare the content to append
        const csvContent = Array.from(doctors).join('\n');

        // Append the unique data to the CSV file (create it if it doesn't exist)
        fs.appendFileSync('doctors.csv', csvContent + '\n');

        res.json({ message: `Data scraped and appended to doctors.csv with ${doctors.size} unique entries` });
    } catch (error) {
        console.error('Failed to scrape data:', error);
        res.status(500).json({ error: 'Failed to scrape data' });
    }
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
