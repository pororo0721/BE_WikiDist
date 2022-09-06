import json


def pull_list(name):
    import requests
    endpoint = 'http://127.0.0.1:5000/#'
    response = requests.get(endpoint)
    data = response.json()

    try:
        data = data['titles'][0]['data']
        title = data['games'][0]['title']
        passfort_data = data['titles'][1]['data']
        passfort_title= data['titles'][1]['title']


        return {'name': name, 'title': title, 'passfort_data': passfort_data, 'passfort_title': passfort_title}
    
    except IndexError:
        return "Doesn't look like we have that in our list"