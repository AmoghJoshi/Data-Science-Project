import pandas as pd

COMMA = ","
NEWLINE = "\n"
EMPTY_STRING = ""
SPACE = " "
HEADER = ""
CURRENCY = "$"
PAGES = "pages"
NAN = "nan"

A = pd.read_csv("Data/books_amazon_clean.csv")
B = pd.read_csv("Data/books_millions_clean.csv")
M = pd.read_csv("Data/matches.csv")

A = A.as_matrix()
B = B.as_matrix()
M = M.as_matrix()

def is_empty_or_nan(value):
    if(not str(value) or str(value) == NAN):
        return True
    return False

def merge_matching_books():
    merged_file = open("Data/merged_data.csv", "w")
    merged_file.write(HEADER)
    for i in range(0, len(M)):
        merged_book = EMPTY_STRING
        aid = M[i][0]
        bid = M[i][1]

        for j in range(1, len(A[aid-1])):
            if(is_empty_or_nan(A[aid-1][j]) and is_empty_or_nan((B[bid-1][j]))):
                merged_book += EMPTY_STRING
                merged_book += COMMA
            elif(is_empty_or_nan(A[aid-1][j])):
                merged_book += str(B[bid-1][j])
                if(j == 6):
                    merged_book += SPACE
                    merged_book += PAGES
                merged_book += COMMA
            elif(is_empty_or_nan(B[bid-1][j])):
                merged_book += str(A[aid-1][j])
                merged_book += COMMA
            elif(j == 4):
                price = str(A[aid-1][j])
                price_amazon = str(A[aid-1][j])
                price_amazon = price_amazon.replace(CURRENCY, EMPTY_STRING)
                price_amazon = price_amazon.strip()
                price_millions = str(B[bid-1][j])
                price_millions = price_millions.replace(CURRENCY, EMPTY_STRING)
                price_millions = price_millions.strip()
                if(float(price_amazon) > float(price_millions)):
                    price = str(B[bid-1][j])
                merged_book += price
                merged_book += COMMA
            elif(j == 6):
                pages = str(A[aid - 1][j])
                pages_amazon = str(A[aid - 1][j])
                pages_amazon = pages_amazon.replace(PAGES, EMPTY_STRING)
                pages_amazon = pages_amazon.strip()
                pages_millions = str(B[bid - 1][j])
                pages_millions = pages_millions.strip()

                if (int(pages_amazon) < int(round(float(pages_millions)))):
                    pages = str(int(round(float(pages_millions))))
                    pages += SPACE
                    pages += PAGES
                merged_book += pages
                merged_book += COMMA
            else:
                merged_book += str(A[aid-1][j])
                merged_book += COMMA

        merged_book = merged_book[0:len(merged_book)-1]
        merged_book += NEWLINE
        merged_file.write(merged_book)
    merged_file.close()

def set_header():
    global HEADER
    amazon_file = open("Data/books_amazon_clean.csv", "r")
    HEADER = amazon_file.readline()
    amazon_file.close()

    first_comma_index = -1
    for i in range(0, len(HEADER)):
        if(HEADER[i] == ','):
            first_comma_index = i
            break;

    HEADER = HEADER[first_comma_index+1:len(HEADER)]



# def integrate_A():
#     global nonmatching_count
#     for a in A:
#         book = EMPTY_STRING
#         if(a[0] in M[:,0]):
#             #print("Match found in integrate A")
#             continue
#         else:
#             for j in range(1, len(a)):
#                 book += str(a[j])
#                 book += COMMA
#         book = book[0:len(book)-1]
#         book += NEWLINE
#         nonmatching_count += 1
#         #print (book)
#
# def integrate_B():
#     global nonmatching_count
#     for b in B:
#         book = EMPTY_STRING
#         if (b[0] in M[:,1]):
#             #print("Match found in integrate B")
#             continue
#         else:
#             for j in range(1, len(b)):
#                 book += str(b[j])
#                 book += COMMA
#         book = book[0:len(book) - 1]
#         book += NEWLINE
#         nonmatching_count += 1
#         #print (book)

set_header()
merge_matching_books()








