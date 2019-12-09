from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import json
import re

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
GOOGLE_API_KEY = 'AIzaSyDH0YkE0qMzSjkYHKt6Xst7pYDnhMiS1pE'
DICTIONARY_API_KEY = 'e45f8b18-26b7-454b-9a5d-869942969c37'

relevant_results = [
    'https://leetcode.com/articles/orderly-queue/',
    'https://massivealgorithms.blogspot.com/2018/11/leetcode-899-orderly-queue.html'
]

paragraphs = []


def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': '001861063061319504683:3lb8itxu6hh',
        'q': query
    }
    response = requests.get(url, params)
    json_response = json.loads(response.text)
    json_response = json_response['items']
    result_links = []
    for x in json_response:
        result_links.append(x['link'])
    return result_links


if __name__ == '__main__':

    tt = ""

    while True:
        print('Enter the paragraph:')
        print("> ", end="")
        query = input()
        if query == ".":
            break
        tt += query + " "
        paragraphs.append(query)

    paragraphs.append(tt)
    for idx in range(len(paragraphs)):
        print("ID: ", idx + 1)
        print(paragraphs[idx])

    # relevant_results = []

    # while True:
    #     print('Enter the relevant links:')
    #     print("> ", end="")
    #     query = input()
    #     if query == ".":
    #         break
    #     tt += query + " "
    #     relevant_results.append(query)

    while True:
        para = int(input("Enter the paragraph id:"))
        if para == -1:
            break
        query = paragraphs[para - 1]
        temp = query

        for q in query.lower():
            if q in punctuations:
                query = query.replace(q, "")

        query = query.split(' ')

        for i in range(len(query)):
            query[i] = query[i].lower()

        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in query if not w in stop_words]
        filtered_sentence = [] 

        for w in query:
            if w not in stop_words:
                filtered_sentence.append(w)

        # print(filtered_sentence) 
        synonyms = []
        words_to_replace = []
        idx = 0
        print("Possible replacements:")

        for word in filtered_sentence:

            if len(word) <= 3:
                continue

            idx += 1
            print()
            print("ID: ", idx, end=' ')
            print("Word to replace: ", word)
            print("List of synonym word:")
            url = "https://api.datamuse.com/words?ml=" + word
            response = requests.request("GET", url)
            json_response = json.loads(response.text)
            t = []
            tt = 0

            for x in json_response[: min(len(json_response) - 1, 5)]:
                tt += 1
                print("id: ", tt, end=' ')
                print("Word to replace: ", x['word'])
                t.append(x['word'])

            synonyms.append(t)      
            words_to_replace.append(word)

        while True:
            user_query = int(input("Enter the id of word to change the word or -1 to exit:"))

            if user_query == -1:
                break

            word_query = int(input("Enter the id of synonym word to change the word or -1 to exit:"))
            print(words_to_replace[user_query - 1], ' ', synonyms[user_query - 1][word_query - 1])
            pattern = re.compile(words_to_replace[user_query - 1], re.IGNORECASE)
            temp = pattern.sub(synonyms[user_query - 1][word_query - 1], temp)
            res = google_search(temp)
            print(res)
            print(temp)
            cnt = 0

            for x in relevant_results:

                if x in res:
                    cnt += 1

            if cnt:
                print(cnt, " common results were found. Replace some words again.")
            else:
                print("No relevant results were found.")
                print("Final string:")
                print(temp)
                break

        