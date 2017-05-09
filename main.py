import psycopg2
import sys


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
                 'Nick names mentors working at Miskolc',
                 'Carol who lost a hat',
                 'The correct Carol',
                 'New Applicant',
                 'Jemima has a new number',
                 'Cancel application request']
    for index, option in enumerate(menu_list):
        print("({0}) {1}".format(index + 1, option))
    print("(0) {0}".format('exit'))


def handle_menu():
    option = int()
    while not option:
        option = input('Select an option: ')
    if option == "1":
        name_of_mentors()
    elif option == "2":
        nick_of_mentors_in_miskolc()
    elif option == "3":
        carols_hat()
    elif option == "4":
        correct_carol()
    elif option == "5":
        new_applicant()
    elif option == "6":
        jeminas_new_number()
    elif option == "7":
        cancel_application()
    elif option == "0":
        sys.exit(0)


def name_of_mentors():
    cur.execute("""SELECT first_name, last_name from mentors""")
    table = cur.fetchall()
    print_table(table)


def nick_of_mentors_in_miskolc():
    cur.execute("""SELECT nick_name from mentors where city='Miskolc'""")
    table = cur.fetchall()
    print_table(table)


def carols_hat():
    pass


def correct_carol():
    pass


def new_applicant():
    pass


def jeminas_new_number():
    pass


def cancel_application():
    pass


def main():
    while True:
        main_menu()
        handle_menu()


if __name__ == '__main__':
    main()
