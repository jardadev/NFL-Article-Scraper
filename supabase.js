const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

const removeDuplicates = async (arr, team) => {
	const { data, error } = await supabase
		.from('articles')
		.select('*')
		.eq('team', team);

	if (error) {
		console.error('Error fetching data from Supabase:', error);
		return arr; // Return the original array in case of an error
	}

	const dbHeadlines = data.map((article) => article.headline);
	const filteredArticles = arr.filter((article) => {
		const duplicates = dbHeadlines.includes(article.headline);
		if (duplicates) {
			console.log(`Duplicate article found: ${article.headline}`);
		}
		return !dbHeadlines.includes(article.headline);
	});
	return filteredArticles;
};

const save = async (articles) => {
	const filteredArticles = await removeDuplicates(articles, articles[0].team);
	const { error } = await supabase.from('articles').insert(filteredArticles);

	if (error) {
		console.error('Error saving data to Supabase:', error);
		return;
	}

	console.log(
		`Saved articles:, ${articles[0].team}[${filteredArticles.length} articles]]]`
	);
};

module.exports = { save };
