import pandas as pd
import matplotlib.pyplot as plt

CURRENCY = "$"
PAGES = "pages"
EMPTY = ""
NAN = "nan"

E = pd.read_csv("Data/merged_data.csv")
E = E.as_matrix()

def pages_vs_price():
    price_list = []
    page_list = []
    isbn_10_list = []

    for i in range(0, len(E)):
        price = str(E[i][3])
        pages = str(E[i][5])
        # isbn_10 = str(E[i][9])
        if(not price or not pages):
            continue
        if(price == NAN or pages == NAN):
            continue

        price = price.replace(CURRENCY,EMPTY)
        price = price.strip()
        pages = pages.replace(PAGES, EMPTY)
        pages = pages.strip()
        price_list.append(float(price))
        page_list.append(float(pages))

    #  Plot graph
    plt.scatter(page_list, price_list, marker='.', c='blue')
    plt.title('pages vs price')
    plt.xlabel('pages')
    plt.ylabel('price')
    plt.show()

    print(page_list)
    print(price_list)

def category_vs_price():
    categories_to_total_price = {}
    categories_to_count = {}
    categories_price_avg = {}

    for i in range(0, len(E)):
        category = str(E[i][1])
        price = str(E[i][3])
        if(not price or price == NAN):
            continue
        price = price.replace(CURRENCY, EMPTY)
        price = price.strip()

        if(not category in categories_to_total_price):
            categories_to_total_price[category] = 0.0
            categories_to_count[category] = 0
        categories_to_total_price[category] += float(price)
        categories_to_count[category] += 1

    # Calculate average price of books per category
    for i in categories_to_count:
        categories_price_avg[i] = round(categories_to_total_price[i] / categories_to_count[i], 2)


    print(categories_to_total_price)
    print(categories_to_count)
    print(categories_price_avg)

def category_vs_pages():
    categories_to_total_pages = {}
    categories_to_count = {}
    categories_page_avg = {}

    for i in range(0, len(E)):
        category = str(E[i][1])
        pages = str(E[i][5])
        if(not pages or pages == NAN):
            continue
        pages = pages.replace(PAGES, EMPTY)
        pages = pages.strip()

        if(not category in categories_to_total_pages):
            categories_to_total_pages[category] = 0.0
            categories_to_count[category] = 0
        categories_to_total_pages[category] += float(pages)
        categories_to_count[category] += 1


    for i in categories_to_count:
        categories_page_avg[i] = round(categories_to_total_pages[i] / categories_to_count[i], 2)


    print(categories_to_total_pages)
    print(categories_to_count)
    print(categories_page_avg)


def language_vs_price():
    languages_to_total_price = {}
    languages_to_count = {}
    languages_price_avg = {}

    for i in range(0, len(E)):
        language = str(E[i][8])
        price = str(E[i][3])
        if(not price or price == NAN):
            continue
        price = price.replace(CURRENCY, EMPTY)
        price = price.strip()

        if(not language in languages_to_total_price):
            languages_to_total_price[language] = 0.0
            languages_to_count[language] = 0
        languages_to_total_price[language] += float(price)
        languages_to_count[language] += 1



    for i in languages_to_count:
        languages_price_avg[i] = round(languages_to_total_price[i] / languages_to_count[i], 2)


    print(languages_to_total_price)
    print(languages_to_count)
    print(languages_price_avg)
#      Plot histogram
    bins = list(languages_price_avg.keys())
    values = list(languages_price_avg.values())
    print(bins)
    print(values)

    plt.plot(bins, values)
    plt.title('Languages vs Avg price')
    plt.xlabel('Language')
    plt.ylabel('Avg price')
    plt.show()


def language_vs_pages():
    languages_to_total_pages = {}
    languages_to_count = {}
    languages_pages_avg = {}
    for i in range(0, len(E)):
        language = str(E[i][8])
        pages = str(E[i][5])
        if(not pages or pages == NAN):
            continue
        pages = pages.replace(PAGES, EMPTY)
        pages = pages.strip()

        if(not language in languages_to_total_pages):
            languages_to_total_pages[language] = 0.0
            languages_to_count[language] = 0
        languages_to_total_pages[language] += float(pages)
        languages_to_count[language] += 1

    for i in languages_to_count:
        languages_pages_avg[i] = round(languages_to_total_pages[i] / languages_to_count[i], 2)


    print(languages_to_total_pages)
    print(languages_to_count)
    print(languages_pages_avg)

    # Plot histogram
    bins = list(languages_pages_avg.keys())
    values = list(languages_pages_avg.values())
    print(bins)
    print(values)

    plt.bar(bins, values)
    plt.title('Languages vs Avg pages')
    plt.xlabel('Language')
    plt.ylabel('Avg pages')
    plt.show()


# pages_vs_price()

# category_vs_price()
# category_vs_pages()
# language_vs_price()
# language_vs_pages()
