# Primer Parcial
## Programación Web III - RESTful Factory

### Antes de Empezar:

1. Realiza un **Fork** de este repositorio:

![Repositorio del Primer Parcial](https://live.staticflickr.com/65535/53639722499_30d33aa30a_z.jpg)

2. Si vas a trabajar en tu equipo local clona el nuevo repositorio resultado del **Fork** y abrelo con **VSCode** o el editor de tu preferencia para trabajar tu solución. También puedes trabajar tu solución en **GitHub Codespaces**.

3. Completa tus datos personales en la siguiente tabla:
    | Nombre   | Apellido   | CI   |
    | -------- | ---------- | ---- |
    | `Julio Erick` | `Picavia Saravia` | `10066133` |

4. Realiza un commit de esta modificación y sube los cambios a tu repositorio remoto ejecutando los siguientes comandos desde la terminal de tu equipo local o desde **GitHub Codespaces**:
    ```bash
    git add .
    git commit -m "datos actualizados"
    git push origin main
    ```
5. En la terminal ejecuta el siguiente comando para instalar las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### Contexto:

Te han contratado como **Junior Back-End Developer** en una startup de comercio electrónico que vende productos físicos y digitales. Tu primera tarea es desarrollar un **API RESTful** que permita administrar la información de las órdenes de compra de los clientes. Las órdenes tiene la siguiente información:
- **id**: Identificador único de la orden.
- **client**: Nombre del cliente que realizó la orden.
- **status**: Estado de la orden (Pendiente, En Proceso, Enviado, Entregado, Cancelado).
- **payment**: Método de pago de la orden (Tarjeta de Crédito, Tarjeta de Débito, Transferencia Bancaria, PayPal, Bitcoin).

Solo los pedidos de tipo **Físico** tienen las siguientes propiedades adicionales:
- **shipping**: Costo de envío.
- **products**: Lista de productos que contiene la orden.

Solo los pedidos de tipo **Digital** tienen las siguientes propiedades adicionales:
- **code**: Código de descarga del producto digital.
- **expiration**: Fecha de expiración del producto digital.

### Tareas:
Construye una **API RESTful** que permita realizar las operaciones **CRUD** sobre las órdenes de compra de los clientes. La **API** debe permitir realizar las siguientes operaciones:

1. Crear una orden de compra de tipo **Física** con los siguientes productos: Camiseta, Pantalón y Zapatos.
2. Crear una orden de compra **Digital** con el código de descarga `ABC123` y fecha de expiración `2022-12-31`.
3. Listar todas las órdenes de compra.
4. Listar todos los pedidos en estado **Pendiente**.
5. Actualizar el estado de una orden de compra por su **id**.
6. Eliminar una orden de compra por su **id**.
7. Crear una orden de tipo **Física** con los siguientes productos: Licuadora, Refrigeradora y Lavadora. 

La **API RESTful** debe estar construida con el patron de diseño **FACTORY** y debe cumplir con los principios de desarrollo de Software **DRY, KISS, YAGNI y la S de SOLID**.

### Rutas y resultados esperados:

1. POST `/orders`
    - Datos a enviar:
        ```json
        {
            "client": "Juan Perez",
            "status": "Pendiente",
            "payment": "Tarjeta de Crédito",
            "shipping": 10.0,
            "products": ["Camiseta", "Pantalón", "Zapatos"],
            "order_type": "Física"

        }
        ```
    - Resultado Esperado:
        ```json
        {
            "id": 1,
            "client": "Juan Perez",
            "status": "Pendiente",
            "payment": "Tarjeta de Crédito",
            "shipping": 10.0,
            "products": ["Camiseta", "Pantalón", "Zapatos"],
            "order_type": "Física"
        }
        ```
2. POST `/orders`
   - Datos a enviar:
        ```json
        {
            "client": "Maria Rodriguez",
            "status": "Pendiente",
            "payment": "PayPal",
            "code": "ABC123",
            "expiration": "2022-12-31",
            "order_type": "Digital"
        }
        ```
    - Resultado Esperado:
        ```json
        {
            "client": "Maria Rodriguez",
            "status": "Pendiente",
            "payment": "PayPal",
            "code": "ABC123",
            "expiration": "2022-12-31",
            "order_type": "Digital"
        }
        ```
3. GET `/orders`
    - Resultado Esperado:
        ```json
        {
            "1": {
                "client": "Juan Perez",
                "status": "Pendiente",
                "payment": "Tarjeta de Crédito",
                "shipping": 10.0,
                "products": ["Camiseta", "Pantalón", "Zapatos"],
                "order_type": "Física"
            },
            "2":{
                "client": "Maria Rodriguez",
                "status": "Pendiente",
                "payment": "PayPal",
                "code": "ABC123",
                "expiration": "2022-12-31",
                "order_type": "Digital"
            }
        }
        ```
4. GET `/orders/?status=Pendiente`
    - Resultado Esperado:
       ```json
       {
           "1": {
               "client": "Juan Perez",
               "status": "Pendiente",
               "payment": "Tarjeta de Crédito",
               "shipping": 10.0,
               "products": ["Camiseta", "Pantalón", "Zapatos"],
               "order_type": "Física"
           },
           "2":{
               "client": "Maria Rodriguez",
               "status": "Pendiente",
               "payment": "PayPal",
               "code": "ABC123",
               "expiration": "2022-12-31",
               "order_type": "Digital"
           }
       }
       ```
5. PUT `/orders/1`
    - Datos a enviar:
        ```json
        {
            "status": "En Proceso"
        }
        ```
    - Resultado Esperado:
        ```json
        {"1":{
            "client": "Juan Perez",
            "status": "En Proceso",
            "payment": "Tarjeta de Crédito",
            "shipping": 10.0,
            "products": ["Camiseta", "Pantalón", "Zapatos"],
            "order_type": "Física"
        }}
        ```
6. DELETE `/orders/1`
    - Resultado Esperado:
        ```json
        {
            "message": "Orden eliminada"
        }
        ```
7. POST `/orders`
    - Datos a enviar:
        ```json
        {
            "client": "Ana Gutierrez",
            "status": "Pendiente",
            "payment": "Tarjeta de Débito",
            "shipping": 20.0,
            "products": ["Licuadora", "Refrigeradora", "Lavadora"],
            "order_type": "Física"
        }
        ```
    - Resultado Esperado:
        ```json
        {
            "client": "Ana Gutierrez",
            "status": "Pendiente",
            "payment": "Tarjeta de Débito",
            "shipping": 20.0,
            "products": ["Licuadora", "Refrigeradora", "Lavadora"],
            "order_type": "Física"
        }
        ```
8.  GET `/orders`
    - Resultado Esperado:
        ```json
        {
            "2":{
                "client": "Maria Rodriguez",
                "status": "Pendiente",
                "payment": "PayPal",
                "code": "ABC123",
                "expiration": "2022-12-31",
                "order_type": "Digital"
            },
            "3":{
                "client": "Ana Gutierrez",
                "status": "Pendiente",
                "payment": "Tarjeta de Débito",
                "shipping": 20.0,
                "products": ["Licuadora", "Refrigeradora", "Lavadora"],
                "order_type": "Física"
            }
        }
        ```
### Entrega:
1. La lógica de la API debe estar en el archivo `server.py` que se encuentra dentro de la carpeta `solution`.
2. La lógica del cliente debe estar en el archivo `client.py` que se encuentra dentro de la carpeta `solution`.
3. Una vez tengas los puntos 1 y 2 completados, realiza un commit con el mensaje "Entrega Final" y sube los cambios a tu repositorio remoto ejecutando los siguientes comandos desde la terminal de tu equipo local o desde **GitHub Codespaces**:

    ```bash
    git add .
    git commit -m "Entrega Final"
    git push origin main
    ```

4. Una vez completado el paso anterior adjunta la **URL** de tu repositorio de **GitHub** en la tarea asignada en **Google Classroom**. 

### Restricciones:

Durante el examen solo puede consultar los siguientes recursos:
- [Patrón de Diseño Factory](https://refactoring.guru/es/design-patterns/factory-method)
- [Documentación Oficial de Python](https://docs.python.org/3/)
- [Documentación de HTTP Server](https://docs.python.org/3/library/http.server.html)
- [Documentación de la biblioteca requests](https://requests.readthedocs.io/en/latest/)
- [Documentación del modulo urllib.parse](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qs)

### IMPORTANTE: 
- **No** se permite el uso de frameworks como Flask, Django, FastAPI, etc.
- **No** se permite el uso de librerías externas que no estén dentro del archivo `requirements.txt`.
- **No** se permite el uso de bases de datos.
- **No** se permite el uso de archivos para almacenar la información.
- La **API** debe ser **RESTful**.
- La API debe cumplir con las operaciones **CRUD**.
- La **API** debe cumplir con las rutas y resultados esperados.
- La estructura de la **API** debe estar construida con el patrón de diseño **FACTORY**.
- La **API** debe cumplir con los principios de desarrollo de Software **DRY, KISS, YAGNI y la S de SOLID**.
- Los ids de las órdenes deben ser únicos y manejados de forma incremental correlativa.
