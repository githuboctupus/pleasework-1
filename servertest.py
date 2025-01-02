import json
import os
import bottle
import Board
import Snake
import json
import stable_baselines3 as sb3
import env
from stable_baselines3 import DQN
global previousstate
@bottle.route('/')
def index():
    return {
        'apiversion':'1'
    }

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ""


@bottle.post('/start')
def start():
    data = bottle.request.json
    print(json.dumps(data))

    return "ok"


@bottle.post('/move')
def move():
    data = bottle.request.json
    move='up'#model.predict
    if data['turn']==0:
        previousstate=data
    else:
        currentstate=data
        envir = env.Env()
        model = DQN.load("snakemodel", env=env)
    #env.Env() set opp move(previousstate, currentstate)

    previousstate=data
    return move


@bottle.post('/end')
def end():
    data = bottle.request.json

    # print(json.dumps(data))

    return "ok"


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )