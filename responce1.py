import requests

def send_json_post_request(country):
    url = 'http://127.0.0.1:8000/api/get_newsdata/'
    data = {
        'country': country
    }

    # Step 1: Make a POST request to save data
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST request successful!")
        print("Response JSON:", response.json())
    else:
        print(f"POST request failed with status code {response.status_code}.")



if __name__ == "__main__":
    send_json_post_request()