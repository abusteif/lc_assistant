import time

from bs4 import BeautifulSoup
import requests

main_url = "https://intercom.help/lawtap/en/"
main_page = requests.get(main_url).text
main_soup = BeautifulSoup(main_page, "lxml")


def get_articles(article_list_link) -> set:
    results = set()
    article_list = requests.get(article_list_link).text
    articles_soup = BeautifulSoup(article_list, "lxml")
    # text = articles_soup.get_text(separator="\n")
    # print(text)
    articles = articles_soup.find_all("section")
    for article in articles:
        if article.id:
            continue
        article_links = article.find_all("a")
        for article_link in article_links:
            results.add(article_link.get("href"))
    return results


def process_embedded_link():
    pass


def process_article(article_link) -> dict:
    article_check = requests.get(article_link)
    if not article_check:
        return {
            "found": False
        }
    article_soup = BeautifulSoup(article_check.text, "lxml")
    print(article_soup.get_text(separator="\n"))

    time.sleep(1)


main_categories = main_soup.find_all(attrs={"dir": "ltr", "id": True})
for cat in main_categories:
    link = cat.find("a").get("href")
    for r in get_articles(link):
        # print(r)
        process_article(r)
        time.sleep(1)
    print("******************************")
