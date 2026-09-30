def create_list():
    return []


def add_element(my_list, element):
    my_list.append(element)
    return my_list

def remove_element(my_list, element):
    for ele in my_list:
        if(ele==element):
            my_list.remove(element)



