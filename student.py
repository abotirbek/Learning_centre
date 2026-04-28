from db_name import get_connection

def insert_student(full_name, phone, age, gender, group_id, is_active, paid_amount):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    insert into student(full_name, phone, age, gender, group_id, is_active, paid_amount) values(%s, %s, %s, %s, %s, %s, %s)''',
                   (full_name, phone, age, gender, group_id, is_active, paid_amount))
    connection.commit()
    cursor.close()
    connection.close()

def get_all_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7])

def get_active_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where is_active = true''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7])

def get_inactive_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where is_active = false''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7])

def get_female_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where gender = \'female\'''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_male_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where gender = \'male\'''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_student_over_18():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where age > 18''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_unpaid_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where paid_amount = 0''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_student_by_phone(phone_number):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student where phone = %s''', (phone_number,))
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_student_payment_info():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, c.price, s.paid_amount, c.price - s.paid_amount from student s
    inner join student_group sg on sg.id = s.group_id
    inner join course c on c.id = sg.course_id''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2])

def get_student_in_debt():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, sg.name, c.name, c.price - s.paid_amount, s.phone from student s
    inner join student_group sg on sg.id = s.group_id
    inner join course c on c.id = sg.course_id
    where c.price - s.paid_amount != 0''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4])

def get_student_without_debt():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, s.phone, sg.name, c.name from student s
    inner join student_group sg on sg.id = s.group_id
    inner join course c on c.id = sg.course_id
    where c.price - s.paid_amount = 0''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3])

def count_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select count(id) from student''')
    data = cursor.fetchone()[0]
    print(data)

def count_in_active_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select count(id) from student where is_active = true''')
    active = cursor.fetchone()[0]
    cursor.execute('''
    select count(id) from student where is_active = false''')
    inactive = cursor.fetchone()[0]
    print(active, inactive)

def count_male_female():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select count(id) from student where gender = \'male\'''')
    male = cursor.fetchone()[0]
    cursor.execute('''
    select count(id) from student where gender = \'female\'''')
    female = cursor.fetchone()[0]
    print(male, female)

def get_highest_student_payment():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select full_name, paid_amount from student order by paid_amount desc limit 1''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def get_most_indebted_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, s.paid_amount from student_group sg 
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id 
    order by c.price - s.paid_amount desc limit 1''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def create_student_full_info():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        create or replace view student_full_info as
        select s.full_name as full_name, s.phone as phone_number, s.age as age, s.gender as gender, 
        s.is_active as is_active, s.paid_amount as paid_amount, sg.name as group_name, c.name as course_name, 
        c.price as course_price, c.price - s.paid_amount as debt from student s
        inner join student_group sg on s.group_id = sg.id
        inner join course c on c.id = sg.course_id''')
        connection.commit()
        cursor.execute('''
        select * from student_full_info''')
        data = cursor.fetchall()
        for d in data:
            print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9])
    finally:
        cursor.close()
        connection.close()