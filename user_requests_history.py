import json

def write_conversation_to_file(data):
    with open('user_convert_requests.json', 'w') as new_file:
        json.dump(data, new_file)


def write_get_info_to_file(data):
    with open('user_requests_currency_info.json', 'w') as new_file:
        json.dump(data, new_file)
