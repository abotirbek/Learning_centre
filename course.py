from db_name import get_connection

def insert_course(name, duration_month, price):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    insert into course(name, duration_month, price) values(%s, %s, %s)''',
                   (name, duration_month, price))
    connection.commit()
    cursor.close()
    connection.close()

def get_all_course():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from course''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1],d[2],d[3])

def get_course_empty_seats():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select c.name, sg.max_students - count(s.id) from student_group sg
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id
    group by c.name, sg.max_students''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def get_course_debtors():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select c.name, count(s.id) from student_group sg
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id
    where c.price - s.paid_amount != 0
    group by c.name''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def get_course_payment():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select c.name, count(s.id)*c.price from student_group sg
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id group by c.name, c.price''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def count_course_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select c.name, count(s.id) from student_group sg
    inner join student s on s.group_id = sg.id
    inner join course c on c.id = sg.course_id group by c.name''')
    data = cursor.fetchall()
    for d in data:
        print(d[0],d[1])

def get_all_course_student(course_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select * from student s
    inner join student_group sg on sg.id = s.group_id
    inner join course c on c.id = sg.course_id
    where c.name  = %s''', (course_name,))
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])

def get_group_course_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, sg.name, c.name from student s
    inner join student_group sg on sg.id = s.group_id
    inner join course c on c.id = sg.course_id''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1], d[2])

def check_course_price():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    create or replace function check_course_price()
    returns trigger as $$
        declare
            course_price numeric;
        begin
            select c.price
            into course_price
            from student_group sg
            inner join course c on c.id = sg.course_id
            where sg.id = new.group_id;
    
            if course_price is null then
                raise exception 'Student group not found or course price is null!';
            end if;
    
            if new.paid_amount > course_price then
                raise exception 'Fee must NOT exceed course price!';
            end if;
            return new;
        end; $$ language plpgsql;''')
    connection.commit()
    cursor.execute('''
    create or replace trigger trg_check_course_price
    before insert or update on student
    for each row
    execute function check_course_price();''')
    connection.commit()
    cursor.close()
    connection.close()