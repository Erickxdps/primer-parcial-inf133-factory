import requests
import json

url = "http://localhost:8000/orders"
headers = {"Content-Type": "application/json"}

physical_order_data = {
    "client": "Juan Perez",
    "status": "Pendiente",
    "payment": "Tarjeta de Crédito",
    "shipping": 10.0,
    "products": ["Camiseta", "Pantalón", "Zapatos"],
    "order_type": "Física"
}
response = requests.post(url, data=json.dumps(physical_order_data), headers=headers)
print("\nPOST /orders")
print(response.json())

digital_order_data = {
    "client": "Maria Rodriguez",
    "status": "Pendiente",
    "payment": "PayPal",
    "code": "ABC123",
    "expiration": "2022-12-31",
    "order_type": "Digital"
}
response = requests.post(url, data=json.dumps(digital_order_data), headers=headers)
print("\nPOST /orders")
print(response.json())

response = requests.get(url, headers=headers)
print("\nGET /orders")
print(response.json())

pending_orders_url = "http://localhost:8000/orders/?status=Pendiente"
response = requests.get(pending_orders_url)
print("\nGET /orders/?status=Pendiente")
print(response.json())

order_id_to_update = 1
update_data = {"status": "Enviado"}
update_url = f"http://localhost:8000/orders/{order_id_to_update}"
response = requests.put(update_url, data=json.dumps(update_data), headers=headers)
print("\nPUT /orders/1")
print(response.json())

order_id_to_delete = 2
delete_url = f"http://localhost:8000/orders/{order_id_to_delete}"
response = requests.delete(delete_url)
print("\nDELETE /orders/2")
print(response.json())
