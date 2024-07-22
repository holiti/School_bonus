import db.postgredb as db
import mail_newsletter as mail
import GUI.tinterface as gui
from conf import main_path
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
    message('',1)

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
    gui.hinp(mes + '\n')

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
def update_path():
    clear_terminal()
    new_path = gui.input_one('Введите новый путь: ') + '/'

    if db.change_path((new_path,)) == 1:
        message(':(',2)
    else:
        message(':)',2)

def back_up():
    clear_terminal()
    file_name = gui.input_one('Введите имя файла: ') + '.csv'
    var_list = db.get_var_list()
    columns = ','.join(db.list_of_column()[1:])

    if var_list == None or len(columns) == 0 or db.back_up(columns) == 1:
        message(':(',2)
        return
    
    try:
        with open(main_path,'r') as file:
            lines = file.readlines()
        with open(var_list[2][1] + file_name,'w') as file:
            file.write(columns + '\n')
            file.writelines(lines)
            file.write(f'{var_list[0][0]},{var_list[1][0]}')
    except Exception as e:
        print(e)
        message(':(',2)
        return
    message(':)',1)

def backup_month():
    while 1:
        clear_terminal()
        ch = gui.back_up_menu()

        match ch:
            case '1':
                back_up()
            case '2':
                update_path()
            case '3':
                break
            case _:
                gui.not_choise()



#SEND REPORT
def convert_list(info_list,column_list) -> str:
    res = info_list[1] + '\n' + f'Норма часов: {info_list[3]} Выполнено: {info_list[4]} Получено: {info_list[5]} руб.\n'
    for i in range(7,len(column_list),2):
        res += f'{column_list[i][1:]}: {info_list[i]} руб. Примечание: {info_list[i + 1]}\n'     
    res += f'Всего: {info_list[6]} руб.'
    return res

def send_mail(pers_id):
    if pers_id < 1:
        return 1
        
    info_list = db.get_persons_list(pers_id)
    if info_list[0] == -1:
        return 1
            
    column_list = db.list_of_column()
    if column_list[0] == -1:
        return 1

    if mail.send_mail(info_list[2],convert_list(info_list,column_list)) == 1:
        return 1
    return 0

def send_one():
    clear_terminal()
    gui.hinp('Введите ФИО работника')

    while 1:
        s = gui.input_one('')
        if s == 'end':
            break
        pers_id = db.exist_person(convert(s))
        if send_mail(pers_id) == 1:
            message(':(',0)
        else:
            message(':)',0)

def send_all():
    clear_terminal()
    message('Идет отправка...',0)
    pers_list = db.list_of_person()

    if len(pers_list) == 1 and pers_list[0] == -1:
        message(':(',0)

    for i in pers_list:
        stat = None
        if send_mail(i[0]) == 1:
            stat = ':('
        else:
            stat = ':)'
        message(i[1] + ' ' + stat,0)
    message('\nОтправка завершена!!',2)

def send_report():
    while 1:
        clear_terminal()
        ch = gui.send_report_menu()

        match ch:
            case '1':
                send_one()
            case '2':
                send_all()
            case '3':
                break
            case _:
                gui.not_choise()



#MAIN
def main():
    db.connect()

    while 1:
        clear_terminal()
        global overload
        overload = max(0,db.check_fond())
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
                ls = db.list_of_column()
                if db.clear_month(ls[7:]) == 1:
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