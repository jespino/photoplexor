import requests

def notify(url, id, success, size=None):
    data = {}
    data['id'] = id
    data['success'] = success
    data['size'] = size
    try:
        requests.post(url, data)
    except requests.exceptions.ConnectionError:
        print "TODO: Loggear esto"
