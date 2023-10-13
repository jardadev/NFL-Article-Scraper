from db.supa_config import supa

TABLE = 'articles'


class Article:
    """
    Represents NFL news article scraped and stored in a database.

    This class provides methods to interact with articles in the database, including
    retrieving, saving, removing, and filtering articles.

    Attributes:
        team_name (str): The name of the NFL team associated with the article.
        headline (str): The headline or title of the article.
        link (str): The URL link to the full article.
        image (str): The URL link to the article's associated image.
        summary (str): A brief summary or excerpt from the article.

    Methods:
        get_all(cls) -> list[Article]:
            Retrieve all articles from the database.

        get_one(cls, article_id: int) -> Article:
            Retrieve a single article from the database by its ID.

        get_by_team(cls, team: str) -> list[Article]:
            Retrieve articles by the team they belong to.

        get_by_column(cls, column: str) -> list[Article]:
            Retrieve articles based on a specific column name.

        save(cls, article_list: list | dict[str, str | int]) -> list[dict[str, str | int]]:
            Save articles to the database, avoiding duplicates.

        remove_duplicate_articles(cls, articles: list) -> list:
            Remove duplicate articles from a list of articles.

        remove(cls, article_id: int):
            Remove an article from the database by its ID.
    """

    def __init__(self, data: dict):
        self.team_name = data['team_name']
        self.headline = data['headline']
        self.link = data['link']
        self.image = data['image']
        self.summary = data['summary']

    @classmethod
    def get_all(cls) -> list[object]:
        """
        Retrieve all articles from the database.

            Returns:
                list[object]: A list of Article objects representing all articles in the database.
        """
        query_results = supa.table(TABLE).select('*').execute()
        articles = [query_results.data]

        return articles

    @classmethod
    def get_one(cls, article_id: int) -> object:
        """
        Retrieve a single article from the database by its ID.

            Args:
                article_id (int): The ID of the article to retrieve.

            Returns:
                object: An Article object representing the retrieved article.
        """
        query_results = supa.table(TABLE).select(
            '*').eq('id', article_id).execute()
        articles = query_results.data
        article = articles[0]

        return article

    @classmethod
    def get_by_team(cls, team: str) -> list[object]:
        """
        Retrieve articles by the team they belong to.

            Args:
                team (str): The name of the team.

            Returns:
                list[object]: A list of Article objects belonging to the specified team.
        """
        team = team.title()
        query_results = supa.table(TABLE).select(
            '*').eq('team_name', team).execute()
        articles = [query_results.data]

        return articles

    @classmethod
    def get_by_column(cls, column: str) -> list[object]:
        """
        Retrieve articles based on a specific column name.

            Args:
                column (str): The name of the column to search for.

            Returns:
                list[object]: A list of Article objects containing data from the specified column.
        """
        column = column.lower()
        query_results = supa.table(TABLE).select(column).execute()
        articles = []

        for article in query_results.data:

            articles.append(article)

        return articles

    @classmethod
    def save(cls, article_list: list[dict]) -> list[dict]:
        """
        Save articles to the database, avoiding duplicates.

            Args:
                article_list (list | dict[str, str | int]): A list of article dictionaries or a single article dictionary.

            Returns:
                list[dict]: A list of dictionaries representing the saved articles' data.
        """
        filtered_articles = cls.__remove_duplicate_articles(article_list)
        data, count = supa.table(TABLE).insert(filtered_articles).execute()

        return data

    @classmethod
    def __remove_duplicate_articles(cls, articles: list) -> list:
        """
        Remove duplicate articles from a list of articles.

            Args:
                articles (list): A list of article dictionaries.

            Returns:
                list: A list of unique article dictionaries after removing duplicates.
        """
        column_articles: list[object] = cls.get_by_column('headline')
        filtered_articles: list[object] = []
        article_headlines = []

        for article in articles:
            for obj in column_articles:
                article_headlines.append(obj['headline'])
            if article['headline'] in article_headlines:
                print(
                    f'Article {article["headline"]} already in database; skipping over this item.')
                continue
            else:
                filtered_articles.append(article)

        return filtered_articles

    @classmethod
    def remove(cls, article_id: int):
        """
        Remove an article from the database by its ID.

            Args:
                article_id (int): The ID of the article to be removed.

            Returns:
                Any: The result of the database operation.
        """
        data = supa.table(TABLE).delete().eq('id', article_id).execute()
        return data
