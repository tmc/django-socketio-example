from django.http import HttpResponse

from socketio_example.models import Message


BACKLONG_LENGTH = 10

def silly_slow_request(num_seconds=1):
    """
    Silly function that runs a pg_sleep to show queries don't block other green
    threads.
    """
    from django.db import connection
    c = connection.cursor()
    c.execute('select pg_sleep(%s);' % num_seconds)


def socketio(request):
    socketio = request.environ['socketio']
    if socketio.on_connect():
        backlog = Message.objects.all()[:BACKLONG_LENGTH]
        socketio.send({'buffer': [{'message': (message.session_id, message.body)} for message in reversed(backlog)]})
        socketio.broadcast({'announcement': socketio.session.session_id + ' connected'})

    while True:
        message = socketio.recv()

        if len(message) == 1:
            message = message[0]
            Message.objects.create(session_id=socketio.session.session_id, body=message)
            message = {'message': [socketio.session.session_id, message]}
            socketio.broadcast(message)
            # after sending a message block in a long query just for kicks
            silly_slow_request()
        else:
            if not socketio.connected():
                socketio.broadcast({'announcement': socketio.session.session_id + ' disconnected'})
                break

    return HttpResponse()
