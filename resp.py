import requests

def send_json_post_request():
    url = 'http://127.0.0.1:8000/save_data/'
    data = {
        'longitude': '-123.1207',
        'latitude': '49.2827',
        'type': 'restaurant',
        'number_of_data': 10
    }

    # Step 1: Make a POST request to save data
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST request successful!")
        print("Response JSON:", response.json())
    else:
        print(f"POST request failed with status code {response.status_code}.")

    # Step 2: Make a DELETE request to remove data with the same latitude, longitude, or type
    delete_url = 'http://127.0.0.1:8000/delete_data/'
    delete_data = {
        'longitude': '-123.1207',
        'latitude': '49.2827',
        'type': 'restaurant'
    }

    delete_response = requests.delete(delete_url, json=delete_data)

    if delete_response.status_code == 200:
        print("DELETE request successful!")
        print("Response JSON:", delete_response.json())
    elif delete_response.status_code == 404:
        print("No matching data found for deletion.")
    else:
        print(f"DELETE request failed with status code {delete_response.status_code}.")

if __name__ == "__main__":
    send_json_post_request()
