import conf as conf
import psycopg2
from sys import exit;

db = None

def connect() :
    global db
    try:
        db = psycopg2.connect(dbname=conf.db_name,host=conf.db_host,port=conf.db_port,user=conf.db_user,password=conf.db_password)
    except Exception as e:
        #need print
        exit()


def clear_month(list_of_colum):
    try:
        with db.cursor() as curr:
            curr.execute('ALTER TABLE main DISABLE TRIGGER hbonus_edit;')
            curr.execute('UPDATE main SET hour_bonus = 0, bonus_sum = 0,completed_hours = 0;')
            curr.execute('ALTER TABLE main ENABLE TRIGGER hbonus_edit;')
            curr.execute('UPDATE variable SET var = 0 WHERE id = 2;')

            for i in list_of_colum:
                if i[0] == 'n':
                    curr.execute(f'UPDATE main SET {i} = 0;')
                elif i[0] == 't':
                    curr.execute(f'UPDATE main SET {i} = NULL;')
    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0



#ADD DEL PERSON
def create_person(info) -> int:
    try:
        with db.cursor() as curr:
            curr.execute('INSERT INTO main(pers_name,required_hours,gmail) VALUES (%s,%s,%s);',info)
    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0

def del_person(info) -> int:
    try:
        with db.cursor() as curr:
            id = exist_person(info)
            if id < 1:
                return 1

            curr.execute('DELETE FROM main WHERE pers_id = %s;',(id,))
    except Exception as e:
        #need print()
        db.rollback()
        return 1
    db.commit()
    return 0


#ADD DEL CATEGORY
def create_category(info):
    try:
        with db.cursor() as curr:
            curr.execute(f'ALTER TABLE main ADD COLUMN {'n' + info} smallint DEFAULT 0, ADD COLUMN {'t' + info} text;')
    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0

def del_category(info):
    try:
        with db.cursor() as curr:
            curr.execute(f'UPDATE main SET bonus_sum = bonus_sum - {info +'n'};')
            curr.execute(f'ALTER TABLE main DROP COLUMN {'n' + info}, DROP COLUMN {'t' + info};') 
    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0


#ADD DEL BONUS
def create_bonus(info):
    pers_id = exist_person(info[0])
    if change('main',f'{'n' + info[1]} = %s, {'t' + info[1]} = %s','pers_id = %s',tuple((info[2],info[3],pers_id))) == 1:
        return 1
    return change('main','bonus_sum = bonus_sum + %s','pers_id = %s',(info[2],pers_id))

def del_bonus(info):
    pers_id = exist_person(info[0])
    if change('main',f'bonus_sum = bonus_sum - {'n' + info[1]}','pers_id = %s',(pers_id,)) == 1:
        return 1
    return change('main',f'{'n' + info[1]} = 0, {'t' + info[1]} = NULL','pers_id = %s',(pers_id,))



#EXIST
def exist_person(info) -> int:
    res = None
    try:
        with db.cursor() as curr:
            curr.execute('SELECT pers_id FROM main WHERE pers_name = %s;',
                (info,))
        
            res = curr.fetchone()[0]
        if res == None:
            return 0
    except Exception as e:
        #need print
        return -1
    return res



#change
def change(table,sets,condition,info) -> int:
    try:
        with db.cursor() as curr:
            curr.execute(f'UPDATE {table} SET {sets} WHERE {condition};',info)
    except Exception as e:
        #need print
        db.rollback()
        return 1
    db.commit()
    return 0

def change_ch1(info) -> int:
    l = list(info)
    l[0] = exist_person(l[0])
    return change('main','completed_hours = %s','pers_id = %s',(l[1],l[0]))

def change_ch2(info) -> int:
    return change('main','completed_hours = %s','pers_id = %s',info)

def change_fond(info) -> int:
    return change('variable','var = %s','id = 1',info)

def change_path(info) -> int:
    return change('variable','var_t = %s','id = 3',info)



#GET LIST
def list_of_person() -> list:
    res = None
    try:
        with db.cursor() as curr:
            curr.execute('SELECT pers_id, pers_name, required_hours FROM main ORDER BY pers_name;')
            res = curr.fetchall()
    except Exception as e:
        #need print
        return None
    return res



#CHECK FOND
def check_fond() -> int:
    max_f = 0
    sum_f = 0
    try:
        with db.cursor() as curr:
            curr.execute('SELECT var FROM variable WHERE id < 3 ORDER BY id;')
            max_f = curr.fetchone()[0]
            sum_f = curr.fetchone()[0]
    except Exception as e:
        #need print
        return -1
    return sum_f - max_f



#SEND MAIL
def get_persons_list(info) -> list:
    res = []
    try:
        with db.cursor() as curr:
            curr.execute('SELECT * FROM main WHERE pers_id = %s',(info,))
            res = curr.fetchone()
        if res == None:
            return [-1]
    except Exception as e:
        #need print
        return [-1]
    return res

def list_of_column() -> list:
    res = []
    try:
        with db.cursor() as curr:
            curr.execute('SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position;',('main',))
            res = [i[0] for i in curr.fetchall()]
        if res == None:
            return [-1]
    except Exception as e:
        #need print
        return [-1]
    return res



#BACK UP
def get_var_list() -> list:
    res = None
    try:
        with db.cursor() as curr:
            curr.execute('SELECT var,var_t FROM variable ORDER BY id;')
            res = curr.fetchall()
    except Exception as e:
        #need print
        return None
    return res

def back_up(columns) -> int:
    try:
        with db.cursor() as curr:
            curr.execute(f'COPY (SELECT {columns} FROM main ORDER BY pers_name) TO %s WITH CSV;',(conf.main_path,))
    except Exception as e:
        #need print 
        return 1
    return 0