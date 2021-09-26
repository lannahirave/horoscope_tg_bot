#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup


types = 'general love family career health tinager flirt amigos'.split()
signs_zodiac = 'aries gemini taurus cancer lion capricorn aquarius pisces virgo libra scorpio sagittarius'.split()
days = 'yesterday today tomorrow week month year'.split()
types_ru = 'Общий Любовный Семейный Карьерный Здоровье Тинейджер Флирт Амигос'.split()
signs_zodiac_ru = 'Овен Близнецы Телец Рак Лев Козерог Водолей Рыбы Дева Весы Скорпион Стрелец'.split()
days_ru = 'Вчера Сегодня Завтра Неделя Месяц Год'.split()


def parse_zodiac1(type: str,  sign: str, day: str,):
    if type in types_ru:
        type, sign, day = translate_ru_to_eng(type, sign, day)
    if type not in types or sign not in signs_zodiac or day not in days:
        print(type, sign, day)
        return "Что-то пошло не так."
    link = f'https://orakul.com/horoscope/astrologic/{type}/{sign}/{day}.html'
    url = requests.get(link)
    soup = BeautifulSoup(url.text, 'html.parser')
    text = ''

    prognosis = soup.find('h2', class_='typehead')
    if prognosis != None:
        for i in prognosis.text.rstrip():
            text += i
        text += '\n'
        for i in prognosis.parent.next_sibling.find_next('p', class_='').text.rsplit():
            text += i + ' '
    return text


def translate_ru_to_eng(type, sign, day):
    if type in types_ru:
        type = types[types_ru.index(type)]
    if sign in signs_zodiac_ru:
        sign = signs_zodiac[signs_zodiac_ru.index(sign)]
    if day in days_ru:
        day = days[days_ru.index(day)]
    return type, sign, day


def main():
    import random
    import time

    random.seed(time.time())
    current_time = time.time()
    k = 10
    while k > 0:
        a, b, c = random.choice(types_ru),random.choice(signs_zodiac_ru), random.choice(days_ru)
        print(parse_zodiac1(a, b, c))
        print(a, b, c)
        time.sleep(0.05)
        k -= 1
    print(time.time() - current_time)


if __name__ == "__main__":
    main()
