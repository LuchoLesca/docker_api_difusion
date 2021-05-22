from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import client, DBInit, getChannels, updateNumberOfSubscribers, publishInChannels, subscribeToChannels, unsubscribeToChannels
import time


app = Flask(__name__, template_folder='templates')
listener = client
DBInit()

@app.route('/')
def index():
    channels_list = getChannels()
    for channel in channels_list:
        updateNumberOfSubscribers(channel)
    return render_template('./channels.html', channels=channels_list)


@app.route('/ToPost')
def toPost():
    channels_list = getChannels()
    return render_template('./toPost.html', channels=channels_list)


@app.route('/publish', methods=['POST'])
def publish():
    if request.method == 'POST':
        message = request.form.get('message').strip()
        channels = request.form.getlist('channels') or []
        if message != "":
            publishInChannels(channels, message)
    return redirect(url_for('toPost'))


@app.route('/sub-unsub', methods=['GET', 'POST'])
def subUnsub():
    ''' Al clickear en subscribe or unsubscribe'''
    if request.method == 'POST':
        selectedChannels = request.form.getlist('channels') or []

        btnsub = request.form.get('btnSub')
        btnunsub = request.form.get('btnUnsub')

        if type(btnsub) is str:
            subscribeToChannels(selectedChannels, listener)
        if type(btnunsub) is str:
            unsubscribeToChannels(selectedChannels, listener)

    return redirect(url_for('client'))


@app.route('/client')
def client():
    channels_list = getChannels()
    return render_template('./client.html', channels=channels_list)


@app.route('/getmessages')
def getmessages():
    messages_list = []
    if listener.channels:
        while True:
            message = listener.get_message()
            if message:
                if message.get('type') == "message":
                    messages_list.append({"channel":message.get("channel"), "message":message.get("data")})
            else:
                break
            time.sleep(0.01)
    return jsonify(messages_list)



if __name__ == "__main__":
    app.run(host="localhost", port="5000")


