require('dotenv').config();
const puppeteer = require('puppeteer');
const NFL_TEAMS = require('./nfl-data');
const { save } = require('./supabase');

async function scrapeBleacherReport() {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
	const page = await browser.newPage();
	for (const team of NFL_TEAMS) {
		const teamArticles = [];
		const teamName = team.name.replaceAll(' ', '-').toLowerCase();
		console.log(teamName);

		// Go to Bleacher Report
		await page.goto(`https://bleacherreport.com/${teamName}`, {
			waitUntil: 'networkidle2',
		});
		await page.keyboard.press('Escape');

		const elements = await page.$$('li.articleSummary');

		// Get the first 5 articles
		const articles = elements.slice(0, 5);

		for (const article of articles) {
			const headline = await article.$eval('h3', (h3) => h3.textContent);
			const link = await article.$eval(
				'div.articleMedia a',
				(a) => a.href
			);
			const image = await article.$eval('div.articleMedia a', (a) => {
				const image = a.querySelector('img');
				return image ? image.getAttribute('image') : null;
			});
			const summary = await article.$eval('div.articleContent', (div) => {
				const description = div.querySelector('p');
				return description ? description.textContent : null;
			});

			teamArticles.push({
				headline,
				link,
				image,
				summary,
				team: teamName,
			});
		}
		save(teamArticles);
	}
	await browser.close();
}

function delay(time) {
	return new Promise((resolve) => setTimeout(resolve, time));
}

async function run() {
	// const interval = 1000 * 60 * 60 * 12; // 12 hours
	const interval = 10000; // 12 hours
	while (true) {
		await scrapeBleacherReport();
		await delay(interval);
	}
}

module.exports = { run };
