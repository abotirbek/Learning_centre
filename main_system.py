from course import (insert_course, get_all_course, get_course_empty_seats, get_course_debtors, get_course_payment,
                    count_course_student, get_all_course_student, get_group_course_student)
from student_group import (insert_group, get_all_group, get_avg_group_age, get_group_payment, count_group_student,
                           get_all_group_student, create_group_statistics, get_group_student)
from student import (insert_student, get_all_student, get_active_student, get_inactive_student, get_female_student,
                     get_male_student, get_student_over_18, get_unpaid_student, get_student_by_phone, get_student_payment_info,
                     get_student_in_debt,  get_student_without_debt, count_student, count_in_active_student, count_male_female,
                     get_highest_student_payment, get_most_indebted_student, create_student_full_info)

def start_project():
    while True:
        choice = int(input('''
------------------------------------------------------------
0 exit                     =    17 Active students         =
1 insert into course       =    18 Inactive students       =
2 insert into group        =    19 Female students         =
3 insert into student      =    20 Male students           =
4 get all students         =    21 Students over 18        =
---------------------------=    22 Unpaid students         =
5 Empty course seats       =    23 Student by phone number =
6 Course debtors           =    24 Student payment info    =
7 Course payment           =    25 Students with debts     =
8 Course student quantity  =    26 Students without debts  =
9 Specific course students =    27 Student quantity        =
10 Course - group- student =    28 Active student quantity =
---------------------------=    29 Male & Female quantity  =
11 Average group age       =    30 Highest payment         =
12 Group payment           =    31 Most indebted student   =
13 Group student quantity  =    32 Student full info       =
14 Specific group students =                               =
15 Group statistics        =                               =
16 Group - student         =                               =
------------------------------------------------------------
Choose: 
'''))
        match choice:
            case 0: break
            case 1:
                name = input('Course name: ')
                duration_month = int(input('Duration month: '))
                price = int(input('Price in UDS: '))
                insert_course(name, duration_month, price)
            case 2:
                get_all_course()
                name = input('Group name: ')
                start_date = input('Start date: ')
                course_id = int(input('Course ID: '))
                max_students = int(input('Maximum students: '))
                insert_group(name, course_id, start_date, max_students)
            case 3:
                get_all_group()
                full_name = input('Student full name: ')
                phone = int(input('Phone number: '))
                age = int(input('Age: '))
                gender = input('Gender (male/female): ')
                group_id = int(input('Group ID: '))
                is_active = bool(input('Is the student active: '))
                paid_amount = int(input('Paid amount: '))
                insert_student(full_name, phone, age, gender, group_id, is_active, paid_amount)
            case 4: get_all_student()
            case 5: get_course_empty_seats()
            case 6: get_course_debtors()
            case 7: get_course_payment()
            case 8: count_course_student()
            case 9:
                get_all_course()
                course_name = input('Course name: ')
                get_all_course_student(course_name)
            case 10: get_group_course_student()
            case 11: get_avg_group_age()
            case 12: get_group_payment()
            case 13: count_group_student()
            case 14:
                get_all_group()
                group_name = input('Group name: ')
                get_all_group_student(group_name)
            case 15: create_group_statistics()
            case 16: get_group_student()
            case 17: get_active_student()
            case 18: get_inactive_student()
            case 19: get_female_student()
            case 20: get_male_student()
            case 21: get_student_over_18()
            case 22: get_unpaid_student()
            case 23:
                phone_number = int(input('Phone number: '))
                get_student_by_phone(phone_number)
            case 24: get_student_payment_info()
            case 25: get_student_in_debt()
            case 26: get_student_without_debt()
            case 27: count_student()
            case 28: count_in_active_student()
            case 29: count_male_female()
            case 30: get_highest_student_payment()
            case 31: get_most_indebted_student()
            case 32: create_student_full_info()
start_project()
