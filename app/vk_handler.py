from app import app
from flask import Flask, request, json
import vk

@app.route('/feedback/bot')
def feedback_bot():
    return 'hello'
