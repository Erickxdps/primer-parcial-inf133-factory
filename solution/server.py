from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Order:
    id_counter = 1

    def __init__(self, client, status, payment, order_type, shipping=None, products=None, code=None, expiration=None):
        self.id = Order.id_counter
        Order.id_counter += 1
        self.client = client
        self.status = status
        self.payment = payment
        self.order_type = order_type
        self.shipping = shipping
        self.products = products
        self.code = code
        self.expiration = expiration

    def to_dict(self):
        order_dict = {
            "client": self.client,
            "status": self.status,
            "payment": self.payment,
            "order_type": self.order_type
        }
        if self.order_type == "Física":
            order_dict["shipping"] = self.shipping
            order_dict["products"] = self.products
        elif self.order_type == "Digital":
            order_dict["code"] = self.code
            order_dict["expiration"] = self.expiration
        return order_dict

class OrderFactory:
    def create_order(self, order_data):
        return Order(**order_data)

class OrderRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.orders = {}
        self.order_factory = OrderFactory()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/orders":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            order_data = json.loads(post_data.decode("utf-8"))
            order = self.order_factory.create_order(order_data)
            self.orders[order.id] = order
            response_data = order.to_dict()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Ruta no encontrada"}).encode("utf-8"))

    def do_GET(self):
        if self.path == "/orders":
            response_data = {str(order_id): order.to_dict() for order_id, order in self.orders.items()}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        elif self.path.startswith("/orders/?status=Pendiente"):
            pending_orders = {str(order_id): order.to_dict() for order_id, order in self.orders.items() if order.status == "Pendiente"}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(pending_orders).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Ruta no encontrada"}).encode("utf-8"))

    def do_PUT(self):
        if self.path.startswith("/orders/"):
            order_id = int(self.path.split("/")[-1])
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)
            update_data = json.loads(put_data.decode("utf-8"))
            if order_id in self.orders:
                order = self.orders[order_id]
                for key, value in update_data.items():
                    setattr(order, key, value)
                response_data = {str(order_id): order.to_dict()}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Orden no encontrada"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Ruta no encontrada"}).encode("utf-8"))

    def do_DELETE(self):
        if self.path.startswith("/orders/"):
            order_id = int(self.path.split("/")[-1])
            if order_id in self.orders:
                del self.orders[order_id]
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Orden eliminada"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Orden no encontrada"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Ruta no encontrada"}).encode("utf-8"))

def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, OrderRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
