import json

def make_post_request(path, test_client, transaction_details):
    res = test_client.post(path, data=json.dumps(transaction_details), content_type='application/json')
    return res
