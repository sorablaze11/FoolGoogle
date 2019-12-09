from flask import Flask, request, Response, jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import json

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
GOOGLE_API_KEY = 'AIzaSyDH0YkE0qMzSjkYHKt6Xst7pYDnhMiS1pE'

app = Flask(__name__)


@app.route('/api/rewriteit', methods=["POST"])
def rewrite_it():
    query = request.json["query"]

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
    
    print(filtered_sentence) 
    synonyms = {}
    
    for word in filtered_sentence:
        if word == "":
            continue
        url = "https://api.datamuse.com/words?ml=" + word
        response = requests.request("GET", url)
        json_response = json.loads(response.text)
        print(word)
        for x in json_response[: min(len(json_response) - 1, 5)]:
            print(x['word'], end=' ')
        print()
    
    return jsonify(query)


@app.route('/api/googlesearch')
def google_search():
    query = request.json["query"]
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
    print(result_links)
    return jsonify(result_links)


if __name__ == '__main__':
    app.run(debug=True)