import json

def make_post_request(path, test_client, data, token):
    res = test_client.post(path, data=json.dumps(data), content_type='application/json', headers={ "api-token": token })
    return res

def make_get_request(path, test_client, token):
    res = test_client.get(path, headers={ "api-token": token })
    return res
