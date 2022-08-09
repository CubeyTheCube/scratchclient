import requests

# Helper function to get lists of data from the API
def get_data_list(all, limit, offset, url, callback, params="", headers={}):
    if all:
        data = []
        offset = 0
        while True:
            res = requests.get(
                f"{url}/?limit=40&offset={offset}{params}", headers=headers
            ).json()
            data += res
            if len(res) != 40:
                break
            offset += 40
        return [callback(item) for item in data]
    else:
        data = requests.get(
            f"{url}/?limit={limit}&offset={offset}{params}", headers=headers
        ).json()
        return [callback(item) for item in data]
