from lab1 import *


def menu():
    ran = 0
    while 0 == int(input("to continue press '0' or any num to exit: ")):
        it = int(input("""
        to insert it - 1:
                  pu - 2:
               buyer - 3:
          update it - 11:
                 pu - 12:
              buyer - 13:
          delete it - 21:
                 pu - 22:
              buyer - 23:
        add random - 100:
         find atts - 200:
          find fts - 300:
             print - 400:
          ------------->:  """))
        if it == 1:
            insert_tuple(insert_scr[0], (int(input("input num of emp-s: ")),
                                         input("input type of products: "),
                                         input("input name: ")))
        elif it == 2:
            insert_tuple(insert_scr[1], (int(input("cores: ")),
                                         int(input("price: ")),
                                         int(input("it: ")),
                                         input("input name: ")))
        elif it == 3:
            insert_tuple(insert_scr[2], (input("input name: "),
                                         int(input("pu: "))))
        elif it == 11:
            update_id(int(input("id: ")), 'id_it', 'it_companies', 'it_name', input("input new name: "))
        elif it == 12:
            update_id(int(input("id: ")), 'pu_id', 'pu', 'pu_name', input("input new name: "))
        elif it == 13:
            update_id(int(input("id: ")), 'b_id', 'buyer', 'b_name', input("input new name: "))
        elif it == 21:
            delete_id("it_companies", "id_it", int(input("id: ")))
        elif it == 22:
            delete_id("pu", "pu_id", int(input("id: ")))
        elif it == 21:
            delete_id("buyer", "b_id", int(input("id: ")))
        elif it == 100:
            ran += 1
            insert_tuple(insert_scr[0], (ran, "pu"+str(ran), "ran_it_"+str(ran)))
            insert_tuple(insert_scr[1], (ran*100, ran*1000, ran, "ranpu"))
            insert_tuple(insert_scr[2], ("I"+str(ran), ran))
        elif it == 200:
            find_company_pu(input("company: "), input("pu: "))
        elif it == 300:
            fulll_find_text(input("pu full name: "))
        elif it == 400:
            print_table()
        else:
            continue


if __name__ == '__main__':
    create_tables()
    menu()
    # insert_tuple(insert_scr[0], (1000, "pu", "intel"))
    # insert_tuple(insert_scr[1], (10, 100, 1, "x100 amd server"))
    # insert_tuple(insert_scr[0], (1000, "pu", "amd"))
    # insert_tuple(insert_scr[1], (10, 100, 2, "y"))
    # insert_tuple(insert_scr[1], (22, 100, 1, "y"))
    # insert_tuple(insert_scr[2], ("I", 1))
    # insert_tuple(insert_scr[2], ("You", 1))
    # delete_id("pu", "pu_id", 2)
    # update_id(1, 'pu_id', 'pu', 'cores', '15')
    # find_company_pu("amd", 'y')
    # fulll_find_text("amd x100 server")
    # print_table()
    destroy_all()
