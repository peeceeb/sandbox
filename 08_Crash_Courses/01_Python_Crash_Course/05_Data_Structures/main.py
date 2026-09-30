import list_ds
import tuple_ds

my_list = list_ds.create_list()
list_ds.add_element(my_list,5)
print(my_list)

my_tuple=tuple_ds.create_tuple([1,2,3,4])
print(tuple_ds.length(my_tuple))