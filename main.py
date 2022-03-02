from bs4 import BeautifulSoup
import requests
import re
import json
import html

SETTINGS_FILE = 'settings.json'

def load_settings():
    data = json.load(open(SETTINGS_FILE))
    return data

def print_results(settings, api_result):
    for i in range(settings['number_questions']):
        question = api_result['items'][i]

        print(f"({question['score']}) {html.unescape(question['title'])} {question['link']} ")
        
        num_answers = min(settings['number_questions'], question['answer_count'])
        answers = sorted(question['answers'], key=lambda d: d['score'], reverse=True)
        answers = sorted(answers, key=lambda d: d['is_accepted'], reverse=True)
        for j in range(num_answers):
            answer = answers[j]
            accepted = "✅" if answer['is_accepted'] else "  "
            print(f"{accepted} {answer['score']} {answer['link']}")
    print("\n")

def request_stackoverflow_api(query):
    settings = load_settings()
    options = "&".join(f"{o}={settings['stackAPI'][o]}" for o in settings['stackAPI']) # Converting the ditc into an url 
    header = {"Content-Type": "json", "charset":"utf-8",'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url = f"https://api.stackexchange.com/2.3/search/advanced?q={query}&site=stackoverflow&{options}"
    
    api_result = requests.get(url, headers=header).json()
    print_results(settings, api_result)

def main():
    print("Welcome, to FindAnError")
    print("You can edit the StackOverflowAPI settings in settings.json according to https://api.stackexchange.com/docs/advanced-search")
    print("Type 'q' to quit\n\n")
    while True:
        inpt = input("Type an error message: ")
        if inpt == 'q':
            break
        request_stackoverflow_api(inpt)

if __name__ == '__main__':
    main()