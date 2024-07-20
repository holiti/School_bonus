from os import system;
from time import sleep;

def message(mess,time):
    print(mess)
    sleep(time)

def not_choise():
    message('Нет такого выбора',2)

def clear_terminal():
    system('clear')

def input_one(message) -> str:
    return input(message)


#START MENU
def start_menu(ov) -> str:
    print("""1 - Редактировать
2 - Отправить отчет 
3 - Сделать cvs копию
4 - Очистить
5 - Выйти
""")
    print(f'Переполнение фонда: {ov}\n')
    return input('Ваш выбор: ')



#CAST MENU
def cast_menu(ov) -> str:
    print("""1 - Добавить/удалить работников
2 - Добавить/удалить категории премий
3 - Добавить/удалить премии
4 - Изменить отработаные часы
5 - Изменить общий фонд
6 - Назад
""")
    print(f'Переполнение фонда: {ov}\n')
    return input('Ваш выбор: ')


#ADD DEl
def add_del(sub,ov) -> str:
    print(f"""1 - Добавить {sub}
2 - Удалить {sub}
3 - Назад
""")
    print(f'Переполнение фонда: {ov}\n')
    return input('Ваш выбо: ')

def hinp(mes):
    print(mes + '\nДля выхода введите \'end\'')


#CHAGE COMPLETED HOURS
def change_ch_menu(ov):
    print("""1 - Для определеного работника
2 - Для каждого работника
3 - Назад
""")
    print(f'Переполнение фонда: {ov}\n')
    return input('Ваш выбор: ')

def send_report_menu():
    print("""1 - Отправить определенному работнику
2 - Отправить всем работникам
3 - Назад
""")
    return input('Ваш выбор: ')