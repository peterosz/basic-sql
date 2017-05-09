import psycopg2
import sys
import os


try:
    con = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")
cur = con.cursor()


def print_table(table):
    border_horizontal = '━'
    border_vertical = '┃'
    border_cross = '╋'
    columns = [list(x) for x in zip(*table)]
    lengths = [max(map(len, map(str, col))) for col in columns]
    rows = border_vertical + border_vertical.join(' {:^%d} ' % length for length in lengths) + border_vertical
    crosses = border_cross + border_cross.join(border_horizontal * (lenght+2) for lenght in lengths) + border_cross
    print(crosses)
    for line in table:
        print(rows.format(*line))
        print(crosses)


def main_menu():
    menu_list = ['Name of Mentors',
                 'Nick names of mentors working at Miskolc',
                 'Carol who lost a hat',
                 'The correct Carol',
                 'New Applicant',
                 'Jemima has a new number',
                 'Cancel application request',
                 'See Mentors Table',
                 'See Applicants Table']
    for index, option in enumerate(menu_list):
        print("({0}) {1}".format(index + 1, option))
    print("(0) {0}".format('Exit'))


def handle_menu():
    option = int()
    while not option:
        option = input('Select an option: ')
    if option == "1":
        os.system('clear')
        name_of_mentors()
    elif option == "2":
        os.system('clear')
        nick_of_mentors_in_miskolc()
    elif option == "3":
        os.system('clear')
        carols_hat()
    elif option == "4":
        os.system('clear')
        not_carol()
    elif option == "5":
        os.system('clear')
        new_applicant()
    elif option == "6":
        os.system('clear')
        jeminas_new_number()
    elif option == "7":
        os.system('clear')
        cancel_application()
    elif option == "8":
        os.system('clear')
        see_mentors_table()
    elif option == "9":
        os.system('clear')
        see_applicants_table()
    elif option == "0":
        sys.exit(0)


def name_of_mentors():
    cur.execute("""SELECT first_name, last_name from mentors;""")
    print_table(table=cur.fetchall())


def nick_of_mentors_in_miskolc():
    cur.execute("""SELECT nick_name from mentors where city='Miskolc';""")
    print_table(table=cur.fetchall())


def add_full_name_column():
    cur.execute("""ALTER TABLE applicants ADD COLUMN full_name VARCHAR(50);""")
    cur.execute("""UPDATE applicants SET full_name = CONCAT(first_name, ' ', last_name);""")


def del_full_name_column():
    cur.execute("""ALTER TABLE applicants DROP COLUMN full_name;""")


def carols_hat():
    add_full_name_column()
    cur.execute("""SELECT full_name, phone_number FROM applicants where first_name = 'Carol';""")
    print_table(table=cur.fetchall())
    del_full_name_column()


def not_carol():
    add_full_name_column()
    cur.execute("""SELECT full_name, phone_number FROM applicants where email LIKE '%@adipiscingenimmi.edu';""")
    print_table(table=cur.fetchall())
    del_full_name_column()


def new_applicant():
    cur.execute("""INSERT INTO applicants (first_name, last_name, phone_number, email, application_code)
                 VALUES ('Markus', 'Schaffarzyk', '003620/725-2666', 'djnovus@groovecoverage.com', '54823');""")
    cur.execute("""SELECT id, first_name, last_name, phone_number, email, application_code
                FROM applicants WHERE application_code = 54823;""")
    print_table(table=cur.fetchall())
    cur.execute("""DELETE FROM applicants WHERE id = '54823';""")


def jeminas_new_number():
    cur.execute("""UPDATE applicants SET phone_number='003670/223-7459'
                WHERE first_name='Jemima' AND last_name='Foreman';""")
    cur.execute("""SELECT first_name, last_name, phone_number FROM applicants
                WHERE first_name='Jemima' AND last_name='Foreman';""")
    print_table(table=cur.fetchall())


def cancel_application():
    cur.execute("""DELETE FROM applicants WHERE email LIKE '%mauriseu.net';""")


def see_mentors_table():
    cur.execute("""SELECT id, first_name, last_name, nick_name, phone_number,
                email, city FROM mentors;""")
    print_table(table=cur.fetchall())


def see_applicants_table():
    cur.execute("""SELECT * FROM applicants;""")
    print_table(table=cur.fetchall())


def main():
    os.system('clear')
    while True:
        main_menu()
        handle_menu()


if __name__ == '__main__':
    main()
