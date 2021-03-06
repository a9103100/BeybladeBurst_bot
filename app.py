import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '335141104:AAHFwKg6xU8lG7ZVelyZ4GAlGz-d2kUmOrk'
WEBHOOK_URL = 'https://9a44e2ef.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'beyblade',
        'product',
        'detail',
        'parts',
        'part',
        'taiwan',
        'pic',
        'hello'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'beyblade',
            'conditions': 'is_going_to_beyblade'
        },
        {
            'trigger': 'advance',
            'source': 'beyblade',
            'dest': 'product',
            'conditions': 'is_going_to_product'
        },
        {
            'trigger': 'advance',
            'source': 'product',
            'dest': 'detail',
            'conditions': 'is_going_to_detail'
        },
        {
            'trigger': 'advance',
            'source': 'detail',
            'dest': 'detail',
            'conditions': 'is_going_to_detail'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'parts',
            'conditions': 'is_going_to_parts'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'hello',
            'conditions': 'is_going_to_hello'
        },
        {
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'taiwan',
            'conditions': 'is_going_to_taiwan'
        },
        {
            'trigger': 'advance',
            'source': 'taiwan',
            'dest': 'taiwan',
            'conditions': 'is_going_to_taiwan'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'pic',
            'conditions': 'is_going_to_pic'
        },
        {
            'trigger': 'advance',
            'source': 'pic',
            'dest': 'pic',
            'conditions': 'is_going_to_pic'
        },
        {
            'trigger': 'advance',
            'source': 'parts',
            'dest': 'part',
            'conditions': 'is_going_to_part'
        },
        {
            'trigger': 'advance',
            'source': 'part',
            'dest': 'part',
            'conditions': 'is_going_to_part'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2',
                'beyblade',
                'product',
                'detail',
                'part',
                'taiwan',
                'pic',
                'hello'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
