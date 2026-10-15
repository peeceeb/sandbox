# --- STARTER CODE ---
raw_order_input = "   priya sharma - ordered: masala_chai (EXTRA GINGER, no sugar) #ID8849   "
regional_label = "अमृततुल्य"

# TODO: Complete the tasks below!

"""
You have a fantastic grasp of string slicing, negative steps (reversing text), and handling Unicode/UTF-8 encoding (great use of `"प्रसन्न"`!).

Let's put those string skills to the test with a real-life challenge: **The Chai Cafe Order Parser & Receipt Generator**.

---

### ☕ The Challenge: The Messy Online Order Parser

When customers order chai online through a messy web form, their input often comes with extra spaces, weird capitalization, and hidden tags. Your job is to clean it up, slice out the important details, and format a professional receipt.

Here is your starter code:

"""
# --- STARTER CODE ---
raw_order_input = "   priya sharma - ordered: masala_chai (EXTRA GINGER, no sugar) #ID8849   "
regional_label = "अमृततुल्य"

# TODO: Complete the tasks below!





### 📋 Your Tasks
"""
1. **The Cleanup Crew (`.strip()` & Case Methods):**
* Clean up the leading and trailing spaces from `raw_order_input` and save it as `clean_order`.
* Print the cleaned order.
"""
cleaned_order=raw_order_input.strip()
print(cleaned_order)


"""
2. **Slicing & Extraction (`.split()` or Slicing):**
* Extract the customer's name from `clean_order`, capitalize it properly (so it reads `"Priya Sharma"`), and print it.
* Extract the order ID (e.g., `"#ID8849"`) from the end of the string and print it.
"""
Customer_Name=cleaned_order[0:12:1].title()
print(Customer_Name)

Customer_Name=str(cleaned_order.split()[0:2]).title()
print(Customer_Name)

Order_id=str(cleaned_order.split()[-1])
print(Order_id)

"""
3. **Text Transformation (`.replace()` & `.upper()`):**
* Extract the chai type (`"masala_chai"`), replace the underscore with a space, and make it uppercase (so it reads `"MASALA CHAI"`). Print it.
"""
Chai_Type=str(cleaned_order.split()[4].replace("_"," ").upper())
print(Chai_Type)


"""
4. **Printer Encoding Check (`.encode()` & `.decode()`):**
* Take the `regional_label` (`"अमृततुल्य"`), encode it into UTF-8 bytes to send to the thermal receipt printer, and then decode it right back into a string. Print the final decoded label to ensure it prints correctly!
""" 

label_txt="अमृततुल्य"
print(f"label_txt{label_txt}")
encoded_label=label_txt.encode("utf-8")
print(f"Non Encoded Label: {encoded_label}")
print(f"Encoded Label: {encoded_label.decode("utf-8")}")
decoded_label=encoded_label.decode("utf-8")
print(f"Decoded Label: {decoded_label}")

"""
Give it a try and share your solution, or let me know if you want to tackle it step-by-step!
"""


print("##################---------Refined Version--------#####################")
raw_order_input = "   priya sharma - ordered: masala_chai (EXTRA GINGER, no sugar) #ID8849   "
regional_label = "अमृततुल्य"

# 1. Cleanup
cleaned_order = raw_order_input.strip()
print(cleaned_order)

# 2. Extraction (Using join for the list slice)
customer_name = " ".join(cleaned_order.split()[0:2]).title()
print(f"Customer: {customer_name}")

order_id = cleaned_order.split()[-1]
print(f"Order ID: {order_id}")

# 3. Text Transformation (.upper() instead of .title())
chai_type = cleaned_order.split()[4].replace("_", " ").upper()
print(f"Chai Type: {chai_type}")

# 4. Encoding Check
encoded_label = regional_label.encode("utf-8")
decoded_label = encoded_label.decode("utf-8")
print(f"Decoded Label: {decoded_label}")