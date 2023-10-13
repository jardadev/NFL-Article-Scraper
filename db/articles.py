from config import supa

TABLE = 'articles'


def save(article_list):
    """
    Save articles to the database, avoiding duplicates.

        Args:
            article_list (list | dict[str, str | int]): A list of article dictionaries or a single article dictionary.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries representing the saved articles' data.
    """
    filtered_articles = remove_duplicate_articles(article_list)
    data, count = supa.table(TABLE).insert(filtered_articles).execute()

    return data


def remove_duplicate_articles(articles):
    """
    Remove duplicate articles from a list of articles.

        Args:
            articles (list): A list of article dictionaries.

        Returns:
            list: A list of unique article dictionaries after removing duplicates.
    """
    query_results: list[object] = supa.table(TABLE).select('headline').execute()
    column_articles = []

    for article in query_results.data:
        column_articles.append(article)

    filtered_articles: list[object] = []
    article_headlines = []

    for article in column_articles:
        for obj in column_articles:
            article_headlines.append(obj['headline'])
        if article['headline'] in article_headlines:
            print(
                f'Article {article["headline"]} already in database; skipping over this item.')
            continue
        else:
            filtered_articles.append(article)

    return filtered_articles
