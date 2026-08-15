from functools import wraps
def my_decorator(func):
    @wraps(func)
    def wrapper():
        print("Before function run")
        func()
        print("After function run")
    return wrapper

@my_decorator
def greet():
    print("Hello from decorators class from chaicode")

greet()

print(greet.__name__)