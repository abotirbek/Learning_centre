from db_name import get_connection

def get_all_group():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student_group''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1],d[2],d[3],d[4])

def get_avg_group_age():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select sg.name, round(avg(s.age)) from student_group sg
    inner join student s on s.group_id = sg.id group by sg.name''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def get_group_payment():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select sg.name, count(s.id)*c.price from student_group sg
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id group by sg.name, c.price''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def count_group_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select sg.name, count(s.id) from student_group sg
    inner join student s on s.group_id = sg.id group by sg.name''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1])

def get_all_group_student(group_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student s
    inner join student_group sg on sg.id = s.group_id
    where sg.name  = %s''', (group_name,))
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])