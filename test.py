import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes" : 1, "name" : 'vtOne', "views" : 1},
        {"likes" : 100, "name" : 'vtTwo', "views" : 1000},
        {"likes" : 10000, "name" : 'vtThree', "views" : 320000}]
 
for i in range(len(data)):
  response = requests.put(BASE + "video/" + str(i), data[i])
  print(response.json())
 
input()
response = requests.get(BASE + "video/2")
print(response.json())

input()
response = requests.patch(BASE + "video/2", {"likes" : 25})
print(response.json())

input()
response = requests.get(BASE + "video/2")
print(response.json())

input()
response = requests.delete(BASE + "video/2")
print(response)

input()
response = requests.get(BASE + "video/2")
print(response.json())


