# Домашнее задание к лекции 3.2 «Работа с библиотекой requests, http-запросы»
# Исходный код для выполнения домашней работы вы найдете на GitHub.
#
# Задача
# Необходимо расширить функцию переводчика так, чтобы она принимала следующие параметры:
#
# путь к файлу с текстом;
# путь к файлу с результатом;
# язык с которого перевести;
# язык на который перевести (по-умолчанию русский).
# У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком. Функция должна
# взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.
#
# Для переводов можно пользоваться API Yandex.Переводчик.

import requests
import os


def input_dir(prompt):
    f = False
    dir_name = ''
    while not f:
        dir_name = input(prompt)
        if len(dir_name) == 0:
            dir_name = os.path.dirname(os.path.abspath(__file__))
        f = os.path.exists(dir_name)
        if not f:
            print('Вы ввели не существующий путь, попробуйте еще раз')
    return dir_name


def input_lang(prompt):
    f = False
    lang = 'ru'
    while not f:
        try:
            lang_n = int(input(prompt))
            if int(lang_n) in [0, 1, 2, 3]:
                f = True
                if lang_n == 1:
                    lang = 'de'
                elif lang_n == 2:
                    lang = 'es'
                elif lang_n == 3:
                    lang = 'fr'
        except ValueError:
            f = False
        if not f:
            print('Пожалуйста, повторите попытку')
    return lang


def load_text(dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    if os.path.exists(file):
        with open(file, encoding='utf-8') as f:
            text = f.read()
    else:
        text = 'Файл ', file, 'не найден'
        print(text)
    return text


def save_text(text, dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    with open(file, "w", encoding='utf-8') as f:
        f.write(text)
    print('Результат перевода сохранен в файле:', file)


def translate_it(text, inlang, outlang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation,
         inlang: language from which to translate,
         outlang: language in which to translate
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {'key': key, 'lang': inlang + '-' + outlang, 'text': text}

    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


if __name__ == '__main__':
    inputdir = input_dir('Введите путь к файлу с текстом (по умолчанию Enter, если файл в рабочей директории):')
    outputdir = input_dir('Введите путь к файлу с результатом (по умолчанию Enter, если файл в рабочей директории):')
    inlang = input_lang('Выберите язык с которого необходимо перевести. 1 - DE, 2 - ES, 3 - FR  : ')
    outlang = input_lang('Выберите язык на который необходимо перевести. 0 - RU, 1 - DE, 2 - ES, 3 - FR  : ')
    a = translate_it(load_text(inputdir, inlang + '.txt'), inlang, outlang)
    save_text(a, outputdir, inlang + '-' + outlang + '.txt')
    pass
