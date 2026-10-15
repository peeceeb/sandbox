"""
A movie theatre sells 157 tickets. Each row has 12 seats.
Write a Python program using variables and f-strings to calculate:
1. The number of completely filled rows using //.
2. The number of tickets in the partially filled row using %.
3. The total number of rows needed to seat everyone.
Your task: Write the code yourself. I'll review your solution and explain any mistakes.
"""


##########################----Response----#################################
print(f"####################----Response----###############################")
seats_per_row=12
tickets_sold=157

print(f"The number of completely filled rows are",tickets_sold//seats_per_row)
print(f"The number of tickets in the partially filled row using %.",tickets_sold%seats_per_row)
print(f"The total number of rows needed to seat everyone. %.",(tickets_sold//seats_per_row)+1)



##########################----Expected----#################################
print(f"####################----Expected----###############################")
full_rows = tickets_sold // seats_per_row
remaining_tickets = tickets_sold % seats_per_row

total_rows = full_rows + (1 if remaining_tickets > 0 else 0)

print(f"Completely filled rows: {full_rows}")
print(f"Tickets in the partially filled row: {remaining_tickets}")
print(f"Total rows needed: {total_rows}")