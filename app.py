from flask import Flask
app=Flask(__name__)
@app.route('/')
def check()
    return "check"
if __name__=="__main__":
    app.run()

