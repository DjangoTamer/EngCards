import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time


def read_text(filename):
    file_lines = []
    with open(filename, 'r') as file:
        for line in file:
            file_lines.append(line.strip().lower())
    return file_lines


def parse_words(url_main, array, limit=0, delay=0.35):
    results_dict = {}
    for word in array:
        word_url = url_main + word
        response = requests.get(word_url)
        soup = BeautifulSoup(response.content, 'lxml')
        transcription = soup.find('span', {'class': 'transcription'})
        translations = soup.find('div', {'class': 't_inline_en'})
        eng_examples = soup.findAll('p', {'class': 'ex_o'}, limit=limit)
        rus_examples = soup.findAll('p', {'class': 'ex_t human'}, limit=limit)
        results_dict[word] = dict(
            [('transcription', transcription.text.strip()),
             ('translation', translations.text),
             ('eng_examples', [i.text.strip() for i in eng_examples]),
             ('rus_examples', [i.text.strip() for i in rus_examples])
             ]
        )
        time.sleep(delay)
    return results_dict


def save_to_json(json_data, filename, folder):
    with open(f'{folder}{filename}.json', 'w') as f:
        json.dump(json_data, f, indent=4)

if __name__ == '__main__':
    words = []
    url_main = 'https://wooordhunt.ru/word/'
    limit_examples = 0  # 0: все доступные примеры использования; >0: желаемое число примеров

    # получение списка слов из текстового файла words.txt
    words = read_text('inputs/words.txt')

    # парсинг по полученным словам
    json_data = parse_words(url_main, words, limit_examples)

    # сохранение в json файл
    current_time = datetime.today().strftime('%Y.%m.%d_%H.%M')
    save_to_json(json_data, current_time, 'results/')

    with open(f'results/{current_time}.json') as f:
        json_file = json.load(f)
        print(json_file)
    #
    # print(json_file)
