from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Szia! Ez a Flask appom már a Renderen fut!"

if __name__ == '__main__':
    app.run()
