from models import Role

def create_role(data_role):
    if data_role:
        try:
            Role.save_role(data_role)
            return 201,"Role creado con exito"
        except Exception as e:
            return 500,f"Error al crear el role {e}"
def create_roles(data_roles):
    if data_roles:
        try:
            Role.save_roles(data_roles)
            return 201,"Roles creados con exito"
        except Exception as e:
            return 500,f"Error al crear los roles {e}"
def get_roles():
    try:
        roles = Role.get_roles()
        return 200,roles
    except Exception as e:
        return 500,f"Error al obtener los roles {e}"

            