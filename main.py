# Code style не по pep8 https://peps.python.org/pep-0008/

import re
import datetime
from collections import OrderedDict  # Імпорт, який не використовується

def create_racer_abbreviations_dict(file_name): # Немає анотацій типів, треба вказати, що file_name це строка,
    # а функція повертає словник ключами якого будуть строки а значеннями - кортежі
    """Retrieves {'abbreviation': (name, team)}" format dict from abbreviations.txt"""  # докстрінг не відповідає дійсності, фукнція повертає словник а не
    # отримує його
    abbreviations_dict = {}
    with open(file_name, 'r') as fn:
        for line in fn:
            matchObj = re.match(r'^(\w+)_([a-zA-Z\s]+)_([a-zA-Z\s]+)$', line) # matchObj - Camel case не використовується для імен змінних,
            # треба використовувати snake case. Також потрібно перевірити що match не повертає None
            # group(1) is abbreviation, i.e 'SVM' # Не інформативний коментар, необхідно видалити
            abbreviations_dict[matchObj.group(1)] = (
                matchObj.group(2),  # name of a pilot
                matchObj.group(3).rstrip(),  # team
            )
    return abbreviations_dict


# Спочатку краще оголосити всі функції, а потім їх використовувати
# {'abbreviation of pilot': ('name of pilot, 'team')}
abbr_dict = create_racer_abbreviations_dict(
    'abbreviations.txt')

# returns timing log from start.log or end.log in {'abbreviation': time} format
# Ящко попередній коментар пояснює роботу функції нижче - її краще оформити як docstring
def retrieve_timings_from_log(file_name):
    timing_log = {}
    with open(file_name, 'r') as fn:
        for line in fn:
            # matches 2 groups: abbreviation of a racer and time
            matchObj = re.match(r'^([A-Z]+).*(\d{2}:\d+:\d+\.\d+)$', line) # Не використовується перевірка на None для matchObj
            # converts time from a string to datetime object
            lap_time = datetime.datetime.strptime(
                matchObj.group(2).rstrip(), '%H:%M:%S.%f')
            # adds key, value to a timing_log
            timing_log[matchObj.group(1)] = lap_time
    return timing_log


start_timings = retrieve_timings_from_log('start.log')
end_timings = retrieve_timings_from_log('end.log')


def sorted_individual_results(start_timings_, end_timings_, abbr_dict_, reverse_order=False): # abbr_dict_ оголошена, але не використовується
    """ 
    Receives start and end timings and returns an OrderedDict with 
    {abbreviations:timedeltas}
    """
    # creating dict with best lap results
    lap_results = {key: end_timings_[key] - start_timings_.get(key, 0)  # у циклі ми перераховуємо ключі із словника start_timings_, тобто ми впевнені,
                   # що всі key знаходяться у словнику start_timings_, тому використання "start_timings_.get(key, 0)" є лишнім, значення
                   # по замовчуванням ніколи не буде використано, напроти ми використовуємо "end_timings_[key]", що призведе до помилки KeyError у випадку якщо
                   # key не знайдеться у словнику end_timings_, тут доцільніше використати end_timings_.get(key, 0)
                   for key in start_timings_.keys()}
    sorted_results = dict( # Не доцільно створювати додаткову змінну sorted_results, можна просто зробити return відсортованного результату
        sorted(lap_results.items(), key=lambda x: x[1], reverse=reverse_order))
    return sorted_results


sorted_lap_results = sorted_individual_results(  # Зайве перенесення рядка
    start_timings, end_timings, abbr_dict)

# prints result board to a console
# Коментар вище повинен бути у вигляді docstring для функції нижче
def print_result_board(sorted_lap_results_):
    counter = 1
    for key, value in sorted_lap_results_.items():
        racer_name = abbr_dict[key][0] # Використання глобальної змінної abbr_dict без її явного визначення в самій функції або передачі її як аргумент
        # є поганою практикою
        team_name = abbr_dict[key][1]
        best_time = str(value)[2:-3] # Маніпуляція зі строковим представленням об'єкта datetime (str(value)[2:-3]) може бути небезпечною, якщо формат часу зміниться
        print(("{: <3} {: <18} | {: <30}  | {}".format(
            str(counter)+'.', racer_name, team_name, best_time)))
        if counter == 15:
            print( # Зайве перенесення рядка
                '----------------------------------------------------------------------')
        counter += 1


print_result_board(sorted_lap_results)