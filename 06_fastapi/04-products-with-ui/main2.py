from fastapi import FastAPI

app=FastAPI()

#@app.get("/")
#def greet():
#    return "Welcome to the Prasanna Website"

@app.get("/")
def print_something():
    return "Kya re Bhosdike"


