import time
from typing import Optional

from bs4 import BeautifulSoup
import requests

main_url = "https://intercom.help/lawtap/en/"
main_page = requests.get(main_url).text
main_soup = BeautifulSoup(main_page, "lxml")
output_file = "articles.txt"
output_folder = "articles"


def get_main_articles(article_list_link: str, q_in: list) -> None:
    article_list = requests.get(article_list_link).text
    articles_soup = BeautifulSoup(article_list, "lxml")

    main_body = articles_soup.find("section", attrs={"data-testid": "main-content"})
    articles = main_body.find_all("section")
    for article in articles:
        article_links = article.find("div").find_all("a", recursive=False)
        for article_a in article_links:
            article_link = article_a.get("href")
            q_in.append(article_link)


def process_embedded_link(link: str) -> Optional[str]:
    if "intercom.help/lawtap" in link:
        return link
    return link.replace("help.lawtap.com", "intercom.help/lawtap") if "help.lawtap.com" in link else None


def get_file_name(url: str) -> str:
    return url.split("/")[-1]
    # return " ".join(url.split("intercom.help/lawtap/en/articles/")[1].split("-")[1:])

def process_article(article_link: str, q_in: list, q_out: list):
    article = requests.get(article_link).text
    article_soup = BeautifulSoup(article, "lxml")
    content = article_soup.find("article")
    a_elements = content.find_all("a")
    for a in a_elements:
        link = a.get("href")
        processed_link = process_embedded_link(link)
        if processed_link and processed_link not in q_in and processed_link not in q_out:
            q_in.append(processed_link)

    content_filtered = content.get_text(separator="\n").split("\n \nRelated articles")[0]
    # with open(output_file, "a", encoding='utf-8') as articles_file:
    #     articles_file.write(content_filtered)
    file_name = get_file_name(article_link)
    with open(f'{output_folder}/{file_name}.txt', "w", encoding='utf-8') as article_file:
        article_file.write(content_filtered)

    time.sleep(1)


main_categories = main_soup.find_all(attrs={"dir": "ltr", "id": True})
# with open(output_file, "w", encoding='utf-8') as articles_file:
#     articles_file.write("")
unprocessed_url_list = []
processed_url_list = []
for cat in main_categories:
    link = cat.find("a").get("href")
    get_main_articles(link, unprocessed_url_list)

while unprocessed_url_list.__len__() > 0:
    url = unprocessed_url_list.pop()
    print(url)
    processed_url_list.append(url)
    process_article(url, unprocessed_url_list, processed_url_list)
    time.sleep(1)
