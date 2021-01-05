import pyodbc
import time
import os

try:
    conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=HP;'
    'Database=bikestores;'
    'Trusted_Connection=yes;'
)
except pyodbc.Error as err:
    print("Couldn't connect")

def buyerdata_insert(conn):
  cursor = conn.cursor()
  print('INPUT YOUR BUYER DATA\n')
  print('1. Children Bicycles\n2. Comfort Bicycles\n3. Cruisers Bicycles')
  print('4. Cyclocross Bicycles\n5. Electric Bikes\n6. Mountain Bikes\n7. Road Bikes\n')

  categoryid = input('choose category number your customer would buy : ') 
  os.system("cls")
  print("there's the bike name who categorize\n")
  for row in cursor.execute("""select product_id as no_product, product_name as productname
                          from production.products 
                          where category_id = ?""", categoryid):
                          print(row.no_product, row.productname)       
  z = input('\npress enter next step  ')

  #input ke orders info
  while(True):
    os.system("cls")
    try :
        for row in cursor.execute('SELECT count(*) as jumlah FROM sales.orders'):
                orderid = row.jumlah + 1

        print('insert bikes buy history')
        staffid = input('input your staff id : ')
        for row in cursor.execute("""select store_id as storeid
                      from sales.staffs
                      where staff_id = ?""", staffid):
                      store_id = row.storeid
        customerid = input("Costumerid : ")
        orderstatus = input("Order status : ")
        orderdate = input("Order date (ex : 2016-01-01) : ")
        requiredate = input("Required date (ex : 2016-01-01) : ")
        if orderstatus == '4':
          shippeddate = input("Shipped date (ex : 2016-01-01) : ")
        elif orderstatus == '3':
          shippeddate = None
        cursor = conn.cursor()
        val = (orderid, customerid, orderstatus, orderdate, requiredate, shippeddate, store_id, staffid)
        cursor.execute("""SET IDENTITY_INSERT sales.orders ON
                            insert into sales.orders(order_id, customer_id, order_status, 
                            order_date, required_date, shipped_date, store_id, staff_id) values (?, ?, ?, ?, ?, ?, ?, ?)
                            SET IDENTITY_INSERT sales.orders OFF """, val)
        conn.commit()
        print('product succes to input')
        z = input('\nPress enter to next step  ')
        break
    except pyodbc.Error as error:
        print("invalid input data")
        time.sleep(2)
        continue

  #input products who buys by order
  itemid = 0
  loop = int(1)
  while (loop == 1):
      os.system("cls")
      print('--next to input another buyer data--')
      try:
          itemid +=1
          productid = input("\nProductid : ")
          for row in cursor.execute("""select list_price as harga
                                  from production.products 
                                  where product_id = ?""", productid):
                                  price = row.harga
          quantity = input("Quantity : ")
          discount = input("Discount (ex : 0.20): ")
          val = (orderid, itemid, productid, quantity, price, discount)
          cursor.execute("""insert into sales.order_items(order_id, item_id, product_id, 
                              quantity, list_price, discount) values (?, ?, ?, ?, ?, ?)
                              """, val)
          conn.commit()
          print('product succes to input')
          loop = int(input('\n1. input again\n0. exit\n\nchoose : '))
      except pyodbc.Error as error:
          print("invalid data")
          time.sleep(2)
          continue
#check stock of product in store
def stock_check(conn):
  cursor = conn.cursor()
  loop = int(1)
  while(loop == 1):
    try:
      os.system("cls")
      storeid = input('input your store id : ')
      productid = input('input productid : ')
      val = (storeid, productid)
      for row in cursor.execute("""select quantity as quantity
                                  from production.stocks
                                  where store_id = ? and product_id = ?""", val):
                                  print("stocks : ", row.quantity)
      loop = int(input('\n1. check again\n0. exit\n\nchoose : '))
    except pyodbc.Error as Error:
      print('invalid data')
      time.sleep(3)
      continue

def customer(conn):
  cursor = conn.cursor()
  os.system("cls")
  choose = input('1. Insert new costumer\n2. Update exist costumer\nchoose : ')
  #insert new costumer data
  if (choose == '1'):
    while(True):
      try :
        os.system("cls")
        for row in cursor.execute('SELECT count(*) as counting FROM sales.customers'):
                      customerid = row.counting + 1
        firstname = input("First name : ")
        lastname = input("Last name : ")
        phone = input("Phone number (ex : (916) 381-6003) : ")
        email = input("Email (ex : debra.burks@yahoo.com) : ")
        street = input("Street : ")
        city = input("City : ")
        state = input("State: ")
        zipcode = input("Zipcode (ex : 14127): ")
        val = (customerid, firstname, lastname, phone, email, street, city, state, zipcode)
        cursor.execute("""SET IDENTITY_INSERT sales.customers ON
                          insert into sales.customers(customer_id, first_name, last_name, 
                          phone, email, street, city, state, zip_code) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                          SET IDENTITY_INSERT sales.customers OFF   """, val)
        conn.commit()
        print('product succes to input')
        z = input('\nPress enter to next step  ')
        break    
      except pyodbc.Error as Error:
        print('invalid data')
        time.sleep(3)
        continue    
  #update customer data   
  elif (choose == '2'):
     while(True):
      try :    
          os.system("cls")
          customerid = input('customerid : ')
          firstname = input("First name : ")
          lastname = input("Last name : ")
          phone = input("Phone number (ex : (916) 381-6003) : ")
          email = input("Email (ex : debra.burks@yahoo.com) : ")
          street = input("Street : ")
          city = input("City : ")
          state = input("State: ")
          zipcode = input("Zipcode (ex : 14127): ")
          val = (firstname, lastname, phone, email, street, city, state, zipcode, customerid)
          cursor.execute("""
                          UPDATE sales.customers SET first_name=?, last_name=?, 
                          phone=?, email=?, street=?, city=?, state=?, zip_code=? 
                          WHERE customer_id=?
                          """, val)
          conn.commit()
          print('product succes to input')
          z = input('\nPress enter to next step  ')
          break
      except pyodbc.Error as Error:
        print('invalid data')
        time.sleep(3)
        continue  

def show_menu(conn):
  os.system("cls")
  print("=== BIKESTORES PROGRAM APPLICATION")
  print("1. Insert Buyer Data")
  print("2. Check Stocks of Product")
  print("3. Customer Info")
  print("4. Kasus yang telah selesai")
  print("0. Keluar")
  print("------------------")
  menu = input("Pilih menu : ")

  os.system("cls")

  if menu == "1":
    buyerdata_insert(conn)
  elif menu == "2":
    stock_check(conn)
  elif menu == "3":
    customer(conn)
  elif menu == "4":
    print('kambing')
  elif menu == "0":
    exit()
  else:
    print("Menu salah!")

if __name__ == "__main__":
  while(True):
    show_menu(conn)
