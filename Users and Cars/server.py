from flask_app import app
# from flask import Flask, render_template, redirect, session, request
from flask_app.controllers import users, cars


if __name__ == "__main__":
    app.run(debug=True)
