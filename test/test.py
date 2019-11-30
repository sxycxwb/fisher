from flask import Flask, current_app

app = Flask(__name__)
with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']


class MyResource:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('close connection')
