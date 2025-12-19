import requests

r = requests.get("https://httpbin.org/get")

print("Status:", r.status_code)
print("IP:", r.json().get("origin"))
print("Headers:", r.json().get("headers"))
print("Args:", r.json().get("args"))
