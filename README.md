# Data Scraping and Price Analysis for Online Book Retail

**Note:** This project is still ongoing. Stay tuned!

It's quite a long story. I wanted to buy a certain book from some online book store on Tokopedia, an e-commerce platform. This particular book store tends to sell used books (only one copy each) at an interesting price: about half of the original price. With that in mind, even more interesting is that the store owner allows for the price to be bargained.

Since I don't have much experience in bargaining, I wondered whether I can make use of my data science skills somehow. In the reviews, I can also see the product description and price, which presumably is the final price after bargaining, while the listed price of books currently up for sale is before bargaining (presumably, because no one has bought it yet so no bargaining has occurred). Those assumptions make sense to me, so I was thinking of performing statistical analysis on the pricing before and after bargaining, including price prediction, so that I can bargain well-informed.

But wait. I don't have the data yet! Well, it's right there technically, but it's not in the nice CSV dataset format I'm familiar with from data science courses at uni.

So first of all, **I sought to create that dataset!**

Or... several datasets. It's not as easy nor quick as I imagined! Some hurdles so far:

1. It's all HTML and I need to construct a table (or several tables). Data scraping is the obvious answer, but then came the question of legality. I checked [Tokopedia's Terms and Conditions](https://www.tokopedia.com/terms) and concluded that automated access to the website is forbidden (so no Selenium!), and... that's pretty much it. So I accessed the website manually, downloaded the HTML of every single page of the store manually (they don't have that many products/books anyway), and only then scraped locally with BeautifulSoup (so no internet connection needed from then on, no requests!).

2. Then of course data scraping itself is quite a challenge, browsing through HTML tags. A lot of tags even have randomized names! Sometimes I have to resort to matching text by regular expressions, such as searching for price by the "Rp" prefix.

3. Tokopedia is general-purpose, so the available information about the books on sale are as much as the seller is willing to provide. In my case, it's just the title, one or two authors each, and several pictures of the copy from various angles, including some random pages. To properly predict prices, I believe I'll need more information, like when the book was published.

    **The answer is data enrichment**, say, sending GET requests to the Google Books API. New problem: querying by title and author alone cannot guarantee that I'd get the right edition. Keep in mind, the store doesn't mention the edition, nor the publication year which would help determine that.
    
    Making full use of the available data and trying to keep things as automated as possible, at first I tried to solve that by building some sort of image similarity classification model, to compare the product thumbnails we have with book thumbnails from Google Books search results; presumably, different editions have different-looking covers, so the chosen search result is that of the highest similarity score. But even then, there is a small chance the specific edition or even any edition of the book is not on Google Books at all! So a threshold also needs to be determined to be sure that it is the same book after all; in the rare case that it isn't, the book would be marked as requiring manual data enrichment.
    
    Unfortunately, the above experiment didn't work out well. About to give up on automation, I then realized: if I were collecting the data manually, I could just snap the book cover with, say, Google Lens, and it'll retrieve the book for me! So instead of building a model from scratch, I could call Gemini API to identify the book and search the details! **This is the approach I'm currently experimenting with.**

Now to really stay clear of legality issues, I am keeping my downloaded HTML files to myself. But the resulting CSVs are available, though for privacy I censored the original store name everywhere (I have been careful in every single commit!).

This data preparation turned out to be a bigger deal than I initially expected. My data analysis with product prices, like I'm used to at uni, will come shortly after. Stay tuned!
