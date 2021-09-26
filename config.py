#!/usr/bin/python3
token = 'API_TOKEN'

types = 'Общий Любовный Семейный Карьерный Здоровье Тинейджер Флирт Амигос'.split()
signs_zodiac = 'Овен Близнецы Телец Рак Лев Козерог Водолей Рыбы Дева Весы Скорпион Стрелец'.split()
days = 'Вчера Сегодня Завтра Неделя Месяц Год'.split()


if __name__=='__main__':
    print(types, signs_zodiac, days, sep='\n')