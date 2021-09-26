#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup


types = 'general love family career health tinager flirt amigos'.split()
signs_zodiac = 'aries gemini taurus cancer lion capricorn aquarius pisces virgo libra scorpius sagittarius virgo'.split()
days = 'yesterday today tomorrow week month'.split()
types_ru = 'Общий Любовный Семейный Карьерный Здоровье Тинейджер Флирт Амигос'.lower().split()


def parse_zodiac1(type:str,  sign: str, day: str,):
    #print(type, sign, day)

    if type.lower() in types_ru:
        type = types[types_ru.index(type)]
    if type not in types or sign not in signs_zodiac or day not in days:
        return "Sth wrong"
    link = f'https://orakul.com/horoscope/astrologic/{type}/{sign}/{day}.html'
    url = requests.get(link)
    soup = BeautifulSoup(url.text, 'html.parser')
    prognosis = soup.find('p', class_='')
    text = ''
    for i in prognosis.text.rsplit():
        text += i + ' '
    return text


def main():
    import random
    import time

    random.seed(time.time())
    current_time = time.time()
    k = 10
    while k > 0:
        a,b,c = random.choice(types), random.choice(signs_zodiac), random.choice(days)
        parse_zodiac1(c,b,a)
        print(a,b,c)
        time.sleep(0.05)
        k -= 1
    print(time.time() - current_time)


if __name__  == "__main__":
    main()