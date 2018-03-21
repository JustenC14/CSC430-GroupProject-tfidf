import string
from web_crawler import web_crawler

if __name__ == "__main__":
    title,body = web_crawler(input('Enter URL: '))
    print(title)
    body.sort()
    print(body)
