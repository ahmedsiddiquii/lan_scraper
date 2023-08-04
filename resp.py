import requests

def send_json_post_request():
    url = 'http://127.0.0.1:8000/save_data/'
    data = {
        'longitude': '-123.1207',
        'latitude': '49.2827',
        'type': 'restaurant',
        'number_of_data': 10
    }
    session = requests.Session()

     # Extract the CSRF token from the cookies

    # Step 2: Make a POST request, including the CSRF token in the headers
    headers = {
        'Referer': url,  # Including the Referer header is often required
    }

    response = session.post(url, json=data,headers=headers)
    # print(response.text)

    if response.status_code == 200:
        print("POST request successful!")
        print("Response JSON:", response.json())
    else:
        print(f"POST request failed with status code {response.status_code}.")

if __name__ == "__main__":
    send_json_post_request()

