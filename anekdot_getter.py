'''
Я бы назвал это парсером, да только я, вероятно, буду использовать API
'''
import ast
import concurrent

import requests
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_joke(ctype=1):
    url = f"http://rzhunemogu.ru/RandJSON.aspx?CType={ctype}"
    try:
        response = requests.get(url)
        text = response.text.encode('utf-8-sig').decode('utf-8-sig')
        #print("\n RAW:", text)
        #print("literal eval:", ast.literal_eval(text))
        #text = text[text.index('{'):text.rindex('}') + 1]
        clean_text = text.replace('\r', '').replace('\n', '').replace('\t', '')
        if '(' in clean_text and ')' in clean_text:
            start = clean_text.index('(') + 1
            end = clean_text.rindex(')')
            clean_text = clean_text[start:end]
        data = json.loads(clean_text)
        # json_text = text[text.index('{'):text.rindex('}') + 1]
        # data = json.loads(json_text)
        return data['content']
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    jokes = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_joke, ctype=i) for i in [11, 1] for _ in range(40000)]
        cnt = 0
        for future in as_completed(futures):
            joke = future.result()

            if joke:
                jokes.append(joke)
            cnt += 1
            if cnt % 100 == 0:
                print("API requests:", cnt)
                print("Actual jokes got:", len(jokes))

    jokes_df = pd.DataFrame(jokes, columns=['joke'])
    jokes_df.to_csv('jokes_dataset.csv', index=False)
    print(jokes_df)


if __name__ == "__main__":
    main()
