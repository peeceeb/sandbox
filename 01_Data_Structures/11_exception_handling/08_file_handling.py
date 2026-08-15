# file=open("order.txt","w")
# try:
#     file.write("Masala Chai - 2cups")
# finally: 
#     file.close()

with open("order.txt", "w") as file:
    file.write("Ginger tea -4cups")
