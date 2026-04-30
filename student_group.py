from db_name import get_connection

def insert_group(name, course_id, start_date, max_students):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    insert into student_group(name, course_id, start_date, max_students) values(%s, %s, %s, %s)''',
                   (name, course_id, start_date, max_students))
    connection.commit()
    cursor.close()
    connection.close()

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

def get_group_student():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    select s.full_name, sg.name from student s 
    inner join student_group sg on sg.id = s.group_id''')
    data = cursor.fetchall()
    for d in data:
        print(d[0], d[1])

def create_group_statistics():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
        create or replace view group_statistics as
        select sg.id as group_id, sg.name as group_name, c.name as course_name, count(s.id) as total_students,
        s.is_active as active_students, s.is_active as inactive_students, sum(s.paid_amount) as total_paid,
        sum(c.price)*count(s.id) - sum(s.paid_amount) as total_debt, sg.max_students - count(s.id) as empty_places
        from student s inner join student_group sg on s.group_id = sg.id
        inner join course c on c.id = sg.course_id group by sg.id, sg.name, c.name, sg.max_students, c.price, s.is_active''')
        connection.commit()
        cursor.execute('''
        select * from group_statistics''')
        data = cursor.fetchall()
        for d in data:
            print(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
    finally:
        cursor.close()
        connection.close()


def check_group_capacity():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    create or replace function check_group_capacity()
    returns trigger as $$
    declare
        current_count int;
        max_allowed int;
    begin
        select max_students
        into max_allowed
        from student_group
        where id = new.group_id;
    
        select count(*)
        into current_count
        from student
        where group_id = new.group_id;
    
        if current_count > max_allowed then
            raise exception 'NO AVAILABLE SPACE LEFT';
        end if;
    
        return new;
    end; $$ language plpgsql;''')
    connection.commit()
    cursor.execute('''
    create or replace trigger trg_check_group_capacity
    before insert or update on student
    for each row
    execute function check_group_capacity();''')
    connection.commit()
    cursor.close()
    connection.close()