import requests

API_BASE_URL= "http://127.0.0.1:5000/" 

print("################  ENDPOINT: itemById  #########################")

print("try to create new item")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "item_count": 1})
print(response.json())
input()

print("try to create new item without required arguments: Expect ERROR")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk"})
print(response.json())
input()

print("try to create item with same ID: Expect ERROR")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "item_count": 1})
print(response.json())
input()

print("try to create item with same Name: Expect ERROR")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/1", {"item_name": "milk", "item_count": 1})
print(response.json())

input()

print("try to get item: Expect SUCCESS")
response = requests.get(API_BASE_URL + "/refrigerator/itemById/0")
print(response.json())
input()

print("try to add one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "differential_item_count": 1})
print(response.json())
input()

print("try to delete one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemById/0", {"differential_item_count": -1})
print(response.json())
input()

print("try to delete two count to item: Expect ERROR as only one item exits in the fridge")
response = requests.put(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "differential_item_count": -2})
print(response.json())
input()

print("try to delete one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "differential_item_count": -1})
print(response.json())
input()

print("try to delete one count to item: Expect ERROR as Item no longer exists")
response = requests.put(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "differential_item_count": -1})
print(response.json())
input()

print("try to get item: ERROR as Item no longer exists")
response = requests.get(API_BASE_URL + "/refrigerator/itemById/0")
print(response.json())
input()

print("try to create a new item")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "egg", "item_count": 12})
print(response.json())
input()

print("delete item completely")
response = requests.delete(API_BASE_URL + "/refrigerator/itemById/0")
print(response)
if response.status_code == 204:
    print("Item deleted")
input()



print("################  ENDPOINT: itemByName  #########################")

print("try to create new item.")
response = requests.post(API_BASE_URL + "/refrigerator/itemByName/milk", {"item_count": 1})
print(response.json())
input()

print("try to create item with same ID: Expect ERROR")
response = requests.post(API_BASE_URL + "/refrigerator/itemByName/milk", {"item_count": 1})
print(response.json())
input()

print("try to get item: Expect SUCCESS")
response = requests.get(API_BASE_URL + "/refrigerator/itemByName/milk")
print(response.json())
input()

print("try to add one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemByName/milk", {"differential_item_count": 1})
print(response.json())
input()

print("try to delete one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemByName/milk", {"differential_item_count": -1})
print(response.json())
input()

print("try to delete two count to item: Expect ERROR as only one item exits in the fridge")
response = requests.put(API_BASE_URL + "/refrigerator/itemByName/milk", {"differential_item_count": -2})
print(response.json())
input()

print("try to delete one count to item: Expect SUCCESS")
response = requests.put(API_BASE_URL + "/refrigerator/itemByName/milk", {"differential_item_count": -1})
print(response.json())
input()

print("try to delete one count to item: Expect ERROR as Item no longer exists")
response = requests.put(API_BASE_URL + "/refrigerator/itemByName/milk", {"differential_item_count": -1})
print(response.json())
input()

print("try to get item: ERROR as Item no longer exists")
response = requests.get(API_BASE_URL + "/refrigerator/itemByName/milk")
print(response.json())
input()

print("try to create a new item")
response = requests.post(API_BASE_URL + "/refrigerator/itemByName/egg", {"item_count": 12})
print(response.json())
input()

print("delete item completely")
response = requests.delete(API_BASE_URL + "/refrigerator/itemByName/egg")
print(response)
if response.status_code == 204:
    print("Item deleted")
input()




print("################  ENDPOINT: allItems  #########################")

print("Create a new item")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/0", {"item_name": "milk", "item_count": 1})
print(response.json())
input()

print("Create a new item")
response = requests.post(API_BASE_URL + "/refrigerator/itemById/1", {"item_name": "egg", "item_count": 1})
print(response.json())
input()

print("Display all items in the refrigerator")
response = requests.get(API_BASE_URL + "/refrigerator/allItems")
print(response.json())
input()

print("Delete all items in the refrigerator")
response = requests.delete(API_BASE_URL + "/refrigerator/allItems")
print(response)
if response.status_code == 204:
    print("All Items deleted")
input()

print("Display all items in the refrigerator to verify delete")
response = requests.get(API_BASE_URL + "/refrigerator/allItems")
print(response.json())
input()



