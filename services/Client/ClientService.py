from models import Client
import datetime as date_time
def create_client(client_data):
    name = ''
    phone = ''
    email = ''
    address = ''
    if client_data:
        if client_data.get('client_name') is None:
            return 400, "El nombre del cliente es requerido"
        else:
            name = client_data.get('client_name')
        if client_data.get('client_phone') is None:
            return 400, "El telefono del cliente es requerido"
        else:
            phone = client_data.get('client_phone')
        if client_data.get('client_email') is None:
            return 400, "El email del cliente es requerido"
        else:
            email = client_data.get('client_email')
        if client_data.get('client_address') is None:
            return 400, "La direccion del cliente es requerida"
        else:
            address = client_data.get('client_address')
        new_client = Client.Client(
            client_name=name,
            client_phone=phone,
            client_email=email,
            client_address=address,
            client_creation_date=date_time.datetime.now()
        )
        try:    
            id = Client.save_client(client_data)
            if id == 0:
                code = 400, message = "Error creando el cliente"
            else:
                code = 201, message = "Cliente creado con exito"
                message = "Client created successfully"
        
        except Exception as e:
            return 500, f"Error creating client: {e}"
    return code, message
def get_clients():
    try:
        clients = Client.get_clients()
        if clients:
            return 200, clients
        else:
            return 404, "No se encontraron clientes"
    except Exception as e:
        return 500, f"Error retrieving clients: {e}"
def get_client(client_name):
    try:
        client = Client.get_client_by_name(client_name)
        if client:
            return 200, client
        else:
            return 404, "No se encontro el cliente"
    except Exception as e:
        return 500, f"Error retrieving client: {e}"