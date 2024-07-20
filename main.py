import db.postgredb as db
import GUI.tinterface as gui
from GUI.tinterface import message,clear_terminal

overload = 0

#CHANGE COMPLETED HOURS
def change_all():
    clear_terminal()
    pers_list = db.list_of_person()
    if len(pers_list) > 0 and pers_list[0] == -1:
        message('Не удалось получить список работников :(',2)
        return
    
    gui.hinp('')
    for i in pers_list:
        h = gui.input_one(f'ФИО: {i[1]} Норма: {i[2]} Выполнено: ')
        if h == 'end':
            break
        if db.change_ch2((h,i[0])) == 1:
            message(':(',0)
        else:
            message(':)',0)

def change_comp_hour():
    while 1:
        clear_terminal()
        global overload
        ch = gui.change_ch_menu(overload)

        match ch:
            case '1':
                big_input(db.change_ch1,'Введите ФИО и отработанные часы')
            case '2':
                change_all()
            case '3':
                break
            case _:
                gui.not_choise()
        overload = max(0,db.check_fond())



#CONVERT
def convert(s) -> tuple:
    l = list(s.split())
    if len(l) == 1:
        return l[0]
    rl = [l[0] + ' ' + l[1] + ' ' + l[2]]
    for i in range(3,len(l)):
        rl.append(l[i])
    return tuple(rl)



#ADD DELETE
def big_input(func,mes):
    clear_terminal()
    gui.hinp(mes)

    while 1:
        s = gui.input_one('')
        if s == 'end':
            break
        if func(convert(s)) == 1:
            message(':(',0)
        else:
            message(':)',0)

def add_del(sub, func1, func2, mes1, mes2):
    while 1:
        clear_terminal()
        global overload
        ch = gui.add_del(sub,overload)

        match ch:
            case '1':
                big_input(func1,mes1)
            case '2':
                big_input(func2,mes2)
            case '3':
                break
            case _:
                gui.not_choise()
        overload = max(0,db.check_fond())



#CAST MENU
def cast_month():
    while 1:
        clear_terminal()
        global overload
        ch = gui.cast_menu(overload)

        match ch:
            case '1':
                add_del('работника',db.create_person,db.del_person,
                    'Введите ФИО, норму часов и gmail','Введите ФИО')
            case '2':
                add_del('категорию',db.create_category,db.del_category,
                    'Введите название категории','Введите название категории')
            case '3':
                add_del('премию',db.create_bonus,db.del_bonus,
                    'Введите ФИО работника, название категории, премию и пояснение','Введите имя работника и категорию')
            case '4':
                change_comp_hour()
            case '5':
                clear_terminal()
                s = gui.input_one('Введите сумму фонда: ')
                if db.change_fond((s,)) == 1:
                    message('Ощибка при изменении :(',2)
                else:
                    message('Фонд изменен :)',1)
                    overload = max(0,db.check_fond())
            case '6':
                break
            case _:
                gui.not_choise()


#BACK UP
def backup_month():
    pass



#SEND REPORT
def send_report():
    pass



#MAIN
def main():
    db.connect()

    while 1:
        clear_terminal()
        global overload
        ch = gui.start_menu(overload)

        match ch:
            case '1':
                cast_month()
            case '2':
                send_report()
            case '3':
                backup_month()
            case '4':
                clear_terminal()
                if db.clear_month() == 1:
                    message('Не удалось очистить месяц... :(',2)
                else:
                    message('Месяц очищен! :)',1)
            case '5':
                break
            case _:
                gui.not_choise()
    clear_terminal()

if __name__ == '__main__':
    main()