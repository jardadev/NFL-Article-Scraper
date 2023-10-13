from bs4 import BeautifulSoup
import requests
from db.articles import Article


class BrScraper:
    """
    A class for scraping NFL news articles from Bleacher Report by team using BeautifulSoup.

    This class provides methods to scrape and parse NFL news articles from Bleacher Report for
    a specified NFL team. It allows you to retrieve headlines, links, images, summaries, and
    the team name for each article.

        Class Attributes:
            BR_NFL_TEAMS (dict): A mapping of NFL team names to their corresponding Bleacher Report URLs.

        Methods:
            scrape_br(cls, team: str = 'bears', limit: int = 10) -> list[dict]:
                Scrapes NFL news articles for a specified team.

                Args:
                    team (str, optional): The name of the NFL team. Defaults to 'bears'.
                    limit (int, optional): The maximum number of articles to scrape. Defaults to 10.

                Returns:
                    list[dict]: A list of dictionaries containing scraped article data.
    """
    BR_NFL_TEAMS = {
        # A mapping of NFL team names to their corresponding Bleacher Report URLs.
        # (This dictionary defines the available teams and their URLs.)
        "49ers": "san-francisco-49ers",
        "Bears": "chicago-bears",
        "Bengals": "cincinnati-bengals",
        "Bills": "buffalo-bills",
        "Broncos": "denver-broncos",
        "Browns": "cleveland-browns",
        "Buccaneers": "tampa-bay-buccaneers",
        "Cardinals": "arizona-cardinals",
        "Chargers": "los-angeles-chargers",
        "Chiefs": "kansas-city-chiefs",
        "Colts": "indianapolis-colts",
        "Commanders": "washington-commanders",
        "Cowboys":  "dallas-cowboys",
        "Dolphins": "miami-dolphins",
        "Eagles": "philadelphia-eagles",
        "Falcons": "atlanta-falcons",
        "Giants": "new-york-giants",
        "Jaguars": "jacksonville-jaguars",
        "Jets": "new-york-jets",
        "Lions": "detroit-lions",
        "Packers": "green-bay-packers",
        "Panthers": "carolina-panthers",
        "Patriots": "new-england-patriots",
        "Raiders": "las-vegas-raiders",
        "Rams": "los-angeles-rams",
        "Ravens": "baltimore-ravens",
        "Saints": "new-orleans-saints",
        "Seahawks": "seattle-seahawks",
        "Steelers": "pittsburgh-steelers",
        "Texans": "houston-texans",
        "Titans": "tennessee-titans",
        "Vikings":  "minnesota-vikings",
    }

    @classmethod
    def scrape_br(cls) -> list[dict]:
        """
        Scrapes NFL news articles for a specified team from Bleacher Report.

            Args:
                team (str, optional): The name of the NFL team. Defaults to 'bears'.
                limit (int, optional): The maximum number of articles to scrape. Defaults to 10.

            Returns:
                list[dict]: A list of dictionaries containing scraped article data.
        """
        parsed_articles: list[dict] = []

        for team in cls.BR_NFL_TEAMS.values():
            br_url = f'https://bleacherreport.com/{team}'
            response = requests.get(br_url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            br_articles = soup.find_all('li', class_='articleSummary', limit=30)

            # Logic for extracting news articles from Bleacher Report html
            for br_article in br_articles:
                headline = br_article.find('h3').text
                link = br_article.find('div', class_='articleMedia').a['href']
                image = br_article.find('div', class_='lazyImage').img['image']
                summary = br_article.find('p', class_='articleDescription')
                if summary:
                    summary = summary.text

                article = {
                    'headline': headline,
                    'link': link,
                    'image': image,
                    'summary': summary,
                    'team_name': team
                }

                parsed_articles.append(article)

            Article.save(parsed_articles)
            print(f'Successfully scraped {len(parsed_articles)} {team} articles.') if parsed_articles\
                else print(f'No articles scraped for {team}')

if __name__ == "__main__":
    print(BrScraper.scrape_br())
