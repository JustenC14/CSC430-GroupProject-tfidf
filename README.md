# Python TF-IDF Website Ranker

This project was created by Justen Caldwell and Brandon Robertson
for the course CSC430 - Information Storage and Retrieval. The program takes a query
and a list of websites from a user. It then uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/ "BeautifulSoup Landing Page") to scrape information from the provided websites and tokenizes the information on these webpages, along with the provided query.

After scraping and tokenizing all of the information, the program then calculates the
tf-idf rankings for all of the websites against the query. Once these tf-idf weights
have been calculated, the program outputs a list. The list is in descending order of how
relevant the information on the page is to the query.

## Future Plans

After many months I would like to revisit this program and attempt to make it
much more useful. Here are some of the things I have planned for this project.
* Ensure that the tf-idf rankings are being calculated properly.
* More complex web-scraper implemenatation.
* Better tokenization of the web-pages and query.
* Create a GUI for the program.
* Create a usage section in the README.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
