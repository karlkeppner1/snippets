import csv, os

def convert_zig_to_tb(zig_orders):
  tb_orders = []
  for order in zig_orders:
    tb_order = {
      "Buy": {
        "Date and Time": "",
        "Transaction Type": "", 
        "Sent Quantity": "",
        "Sent Currency": "", 
        "Sending Source": "zignaly", 
        "Received Quantity": "", 
        "Received Currency": "", 
        "Receiving Destination": "zignaly", 
        "Fee": "", 
        "Fee Currency": "USD", 
        "Exchange Transaction ID": "",
        "Blockchain Transaction Hash": ""
      },
      "Sale": {
        "Date and Time": "",
        "Transaction Type": "", 
        "Sent Quantity": "",
        "Sent Currency": "", 
        "Sending Source": "zignaly", 
        "Received Quantity": "", 
        "Received Currency": "", 
        "Receiving Destination": "zignaly", 
        "Fee": "", 
        "Fee Currency": "USD", 
        "Exchange Transaction ID": "",
        "Blockchain Transaction Hash": ""
      }
    }
    try:
      if order["SIDE"] == "LONG":
        if len(order["OPEN DATE"]) == 10:
          tb_order["Buy"]["Date and Time"] = order["OPEN DATE"] + "T00:00:00Z"
        else:
          tb_order["Buy"]["Date and Time"] = order["OPEN DATE"]      
        tb_order["Buy"]["Transaction Type"] = "Buy"
        tb_order["Buy"]["Sent Quantity"] = str(round(float(order["INVESTED"]), 2))
        tb_order["Buy"]["Sent Currency"] = "USD"
        tb_order["Buy"]["Received Quantity"] = order["AMOUNT"]
        tb_order["Buy"]["Received Currency"] =  order["PAIR"].rsplit("USDT")[0]
        tb_order["Buy"]["Fee"] = str(round(abs((float(order["FEES"]) + float(order["FUNDING FEES"]))), 2))
        tb_order["Buy"]["Exchange Transaction ID"] = f'b-{order["ID"]}'
        if len(order["CLOSE DATE"]) == 10:
          tb_order["Sale"]["Date and Time"] = order["CLOSE DATE"] + "T00:00:00Z"
        else:
          tb_order["Sale"]["Date and Time"] = order["CLOSE DATE"] 
        tb_order["Sale"]["Transaction Type"] = "Sale"
        tb_order["Sale"]["Sent Quantity"] = order["AMOUNT"]
        tb_order["Sale"]["Sent Currency"] = order["PAIR"].rsplit("USDT")[0]
        tb_order["Sale"]["Received Quantity"] = str(round(float(order["AMOUNT"]) * float(order["AVERAGE EXIT PRICE"]), 2))
        tb_order["Sale"]["Received Currency"] = "USD"
        tb_order["Sale"]["Fee"] = "0"
        tb_order["Sale"]["Exchange Transaction ID"] = f's-{order["ID"]}'
      elif order["SIDE"] == "SHORT":
        if len(order["CLOSE DATE"]) == 10:
          tb_order["Buy"]["Date and Time"] = order["CLOSE DATE"] + "T00:00:00Z"
        else:
          tb_order["Buy"]["Date and Time"] = order["CLOSE DATE"]      
        tb_order["Buy"]["Transaction Type"] = "Buy"
        tb_order["Buy"]["Sent Quantity"] = str(round(float(order["AMOUNT"]) * float(order["AVERAGE EXIT PRICE"]), 2))
        tb_order["Buy"]["Sent Currency"] = "USD"
        tb_order["Buy"]["Received Quantity"] = order["AMOUNT"]
        tb_order["Buy"]["Received Currency"] =  order["PAIR"].rsplit("USDT")[0]
        tb_order["Buy"]["Fee"] = str(round(abs((float(order["FEES"]) + float(order["FUNDING FEES"]))), 2))
        tb_order["Buy"]["Exchange Transaction ID"] = f'b-{order["ID"]}'
        if len(order["OPEN DATE"]) == 10:
          tb_order["Sale"]["Date and Time"] = order["OPEN DATE"] + "T00:00:00Z"
        else:
          tb_order["Sale"]["Date and Time"] = order["OPEN DATE"]
        tb_order["Sale"]["Transaction Type"] = "Sale"
        tb_order["Sale"]["Sent Quantity"] = order["AMOUNT"]
        tb_order["Sale"]["Sent Currency"] = order["PAIR"].rsplit("USDT")[0]
        tb_order["Sale"]["Received Quantity"] = str(round(float(order["INVESTED"]), 2))
        tb_order["Sale"]["Received Currency"] = "USD"
        tb_order["Sale"]["Fee"] = "0"
        tb_order["Sale"]["Exchange Transaction ID"] = f's-{order["ID"]}'
      else:
        print("Invalid order, skipping the following order.", order)
      tb_orders.append(tb_order["Buy"])
      tb_orders.append(tb_order["Sale"])
    except:
      print("Invalid order, skipping the following order.", order)
      continue
  return tb_orders

def import_csvs(dir_abspath):
  orders = []
  for file in os.listdir(dir_abspath):
    with open (os.path.join(dir_abspath, file), 'r') as f:
      reader = csv.DictReader(f)
      for order in reader:
        orders.append(order)
  return orders

def write_to_file(orders, filename):
  with open (filename, 'w') as f:
    csv_writer = csv.DictWriter(f, orders[0].keys())
    csv_writer.writeheader()
    for order in orders:
      csv_writer.writerow(order)
  print(f"Taxbit CSV has been written. {os.path.join(os.getcwd(),filename)}")
  return

if __name__ == "__main__":
  print("Please enter the relative path to the directory holding your Zignaly CSV dumps.")
  dir_path = input()
  zig_orders = import_csvs(os.path.join(os.getcwd(), dir_path))
  tb_orders = convert_zig_to_tb(zig_orders)
  write_to_file(tb_orders, "taxbit.csv")
