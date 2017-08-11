import os

from bottle import get, route, request, response, run, post
sys.path.insert(0, os.path.abspath('..'))

from helpers import motor

robot = motor.Motor()


def handle_padded(handler):
    def decorator(**kwargs):
        r = handler
        try:
            callback = request.query.get('callback')
        except Exception as e:
            callback = None
        if callback is None:
            return r(kwargs)
        else:
            response.content_type = 'text/javascript'
            return "%s(%r);" % (callback, r)

    return decorator


@get('/Robot___init__/<addr>/<left_id>/<right_id>/<left_trim>/<right_trim>/<stop_at_exit>')
@handle_padded
def Robot___init__(kargs):
    r = {'return_value': robot.__init__()}
    return r


@get('/Robot__left_speed/<speed>')
@handle_padded
def Robot__left_speed(kargs):
    r = {'return_value': 0}
    return r


@get('/Robot__right_speed/<speed>')
@handle_padded
def Robot__right_speed(kargs):
    r = {'return_value': 0}
    return r


@get('/Robot_stop')
@handle_padded
def Robot_stop(kargs):
    r = {'return_value': robot.stop()}
    return r


@get('/Robot_forward/<speed>/<seconds>')
@handle_padded
def Robot_forward(kargs):
    r = {'return_value': robot.forward()}
    return r


@get('/Robot_backward/<speed>/<seconds>')
@handle_padded
def Robot_backward(kargs):
    r = {'return_value': robot.backward()}
    return r


@get('/Robot_right/<speed>/<seconds>')
@handle_padded
def Robot_right(kargs):
    r = {'return_value': robot.right()}
    return r


@get('/Robot_left/<speed>/<seconds>')
@handle_padded
def Robot_left(kargs):
    r = {'return_value': robot.left()}
    return r


@get('/Robot_left_glide/<speed>/<seconds>')
@handle_padded
def Robot_left_glide(kargs):
    r = {'return_value': robot.rotate_left()}
    return r


@get('/Robot_right_glide/<speed>/<seconds>')
@handle_padded
def Robot_right_glide(kargs):
    r = {'return_value': robot.rotate_right()}
    return r


run(host='0.0.0.0', port=8080, debug=True)
