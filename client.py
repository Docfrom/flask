import requests

# response = requests.post(
#     "http://127.0.0.1:5000/user/",
#     json={'name': 'user_2', 'password': '1234'},
# )

# response = requests.get(
#     "http://127.0.0.1:5000/user/1")
#
# print(response.status_code)
# print(response.json())

response = requests.patch(
    "http://127.0.0.1:5000/user/1", json={"name": "new_name_3", "password": "11111"})
#
print(response.status_code)
print(response.json())
# response = requests.get(
#     "http://127.0.0.1:5000/user/1")
#
# print(response.status_code)
# print(response.json())