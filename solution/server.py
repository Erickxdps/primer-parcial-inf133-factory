from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse
#simulacion de base de datos
compras={}


#Clase principal de la compra
class Compra:
    #elinit
    def __init__(self,client,status,payment,order_type):
        self.client=client
        self.status=status
        self.payment=payment
        self.order_type=order_type


#en caso de ser compra digital
class Digital(Compra):

    def __init__(self, client, status, payment, code, expiration):
        super().__init__(client, status, payment,"Digital")
        self.code=code
        self.expiration=expiration



#en caso de ser compra fisica
class Fisico(Compra):

    def __init__(self, client, status, payment, shipping, products):
        super().__init__( client, status, payment,"Fisica")
        self.shipping=shipping
        self.products=products


class OrderFactory:

    @staticmethod
    def create_compra(order_type,client,status,payment,shipping,products,code,expiration):

        if order_type=="Fisica":
            return Fisico(client,status,payment,shipping,products)
        elif order_type=="Digital":
            return Digital(client,status,payment,code,expiration)
        else:
            raise ValueError("Tipo de compra no valida")
        
class CompraService:
    def __init__(self):
        self.factory=OrderFactory()

    def anadir_compra(self,data):
        order_type=data.get('order_type',None)
        client=data.get('client',None)
        status=data.get('status',None)
        payment=data.get('payment',None)
        shipping=data.get('shipping',None)
        products=data.get('products',None)
        code=data.get('code',None)
        expiration=data.get('expiration',None)
        #creando compra
        nuevo=self.factory.create_compra(order_type,client,status,payment,shipping,products,code,expiration)
        if not compras:
            compras[1]=nuevo
        else:
            #solucion al len con el ID
            id=max(compras.keys())+1
            compras[id]=nuevo
        return nuevo.__dict__
    #mostrar las compras
    def mostrar_compras(self):
        return {index:
            compra.__dict__ for index,compra in compras.items()}
    #eliminar por id
    def eliminar_id(self,id):
        lista=self.mostrar_compras().items()
        for i,j in lista:
            if i==id:
                del compras[i]
                return {"message":"Orden eliminada"}
        return None
    #buscar por status
    def buscar_stat(self,status):
        list = {}
        lista = self.mostrar_compras().items()
        for i, j in lista:
            if j['status']==status:
                list[i]=j
        return list
    #actualizacion del id
    def update_id(self,id,data):
        status=data.get('status',None)
        lista=self.mostrar_compras().items()
        for i, j in lista:
            if i==id:
                j['status']=status
                return j
        return None



class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class CompraHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=CompraService()
        super().__init__(*args,**kwargs)

    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path=="/orders/":
            #GET por estado de la compra:
            if 'status' in query_params:
                status = query_params['status'][0]
                nemo = self.controller.buscar_stat(status)
                if nemo:
                    HTTPResponseHandler.response_handler(self,200,nemo)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"No existe el estado"})
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
        elif parsed_path.path == "/orders":
            HTTPResponseHandler.response_handler(self,200,self.controller.mostrar_compras())
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
        

    def do_POST(self):
        if self.path=="/orders":
            data = HTTPResponseHandler.read_data(self)
            siuuuu = self.controller.anadir_compra(data)
            HTTPResponseHandler.response_handler(self,201,siuuuu)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/orders/"):
            id = int(self.path.split("/")[-1])
            ahita = HTTPResponseHandler.read_data(self)            
            compra = self.controller.update_id(id,ahita)
            if compra:
                HTTPResponseHandler.response_handler(self,200,compra)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/orders/"):
            id = int(self.path.split("/")[-1])
            borrao = self.controller.eliminar_id(id)
            if borrao:
                HTTPResponseHandler.response_handler(self,200,borrao)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encotrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

def main(port=8000):
    try:
        server_adress=('',port)
        httpd = HTTPServer(server_adress,CompraHandler)
        print(f'Iniciando el server en el puerto {port}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el server")
        httpd.socket.close()

if __name__ == "__main__":
    main()
