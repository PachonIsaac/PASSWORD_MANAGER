# PASSWORD MANAGER

PASSWORD MANAGER es una API sencilla creada con fastAPI en Python para manejar claves seguras para un usuario. La API se conecta a una base de datos hecha con SQLite que tiene dos tablas, user y password, así se almacenan los datos del usuario y las contraseñas de los mismos.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Documentación de la API](#documentación-de-la-api)

## Requisitos

# Python
Asegúrate de tener Python instalado en tu sistema. Puedes descargar la última versión desde python.org.

# Entorno virtual (Opcional pero recomendado)
Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto. Puedes crear y activar un entorno virtual de la siguiente manera:

```bash
# Instalar virtualenv
pip install virtualenv

# Crear un entorno virtual
python -m venv venv


```


## Instalación
Para la correcta instalación de la API se debe tener instalado Python 3.8 o superior y pip. Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto. Puedes crear y activar un entorno virtual de la siguiente manera:

```bash
# Activar el entorno virtual
# En Windows
.\venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

# Dependencias del proyecto
Una vez que tengas tu entorno virtual activado, instala las dependecias del proyecto utilizando "requirements.txt"
```bash
pip install -r requirements.txt
```

## Ejecución
Puedes ejecutar la aplicacion con el siguiente comando:
```bash
uvicorn main:app --reload
```
Este comando asume que el punto de entrada de tu aplicación es main y la instancia de la aplicación es app. Ajusta según sea necesario.

La aplicación estará disponible en http://127.0.0.1:8000/. Puedes acceder a la documentación de la API en http://127.0.0.1:8000/docs

## Documentación de la API

# Descripción
Esta API proporciona servicios relacionados con la gestion de usuarios autirozados. La autenticación se realiza mediante un token JWT que se obtiene al hacer login. Los servicios que se ofrecen son los siguientes:

# Servicios de usuario
- Crear un usuario
    Para crear un usuario se debe hacer una petición POST a la ruta /users con el siguiente cuerpo:
    ```bash
    {
        "username": "admin",
        "password": "1234"
    }
    ```

- Obtener todos los usuarios
    Para obtener todos los usuarios se debe hacer una petición GET a la ruta /users
    Este metodo solo puede ser accedido por un usuario con rol de administrador, y se la fase de desarrollo se implementó para verificar los datos de los usuarios en la base de datos.
    
- Eliminar un usuario
    Para eliminar un usuario se debe hacer una petición DELETE a la ruta /users/{username}, cabe resaltar que cada usuario tiene un atributo disabled que indica si el usuario esta deshabilitado o no, por lo que al eliminar un usuario se cambia el valor de este atributo a True.

- Recuperar un usuario
    Para recuperar un usuario se debe hacer una petición PUT a la ruta /users/{username}, cabe resaltar que cada usuario tiene un atributo disabled que indica si el usuario esta deshabilitado o no, por lo que al recuperar un usuario se cambia el valor de este atributo a False.


# Autenticación
Para poder acceder a los servicios de la API es necesario autenticarse, teniendo en cuenta que ya se creo el usuario. Para ello se debe hacer una petición POST a la ruta /login con el siguiente cuerpo:
```bash
{
    "username": "admin",
    "password": "1234"
}
```
Si el usuario y la contraseña son correctos, se obtendrá un token JWT que se debe utilizar para acceder a los servicios de la API. Además todo el proceso de seguridad se implementó gracias a el OAuth2PasswordBearer de fastAPI. Para mayor información sobre el proceso de autenticación se puede consultar la documentación de fastAPI. https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/

# Servicios de contraseña
Para acceder a cualquiera de los servicios de contraseña, el usuario debe haber hecho previamente un login, de lo contrario no podrá acceder a ellos. Además gracias a el Depends de fastAPI, se verifica que el token JWT sea valido y se captura la información del usuario que realiza la solicitud.

- Consultar las contraseñan
    Para consultar las contraseñas se debe hacer una petición GET a la ruta /passwords, conociendo el usuario que lo solicita mediante get_current_user se busca todas las contraseñas que tenga el usuario en la base de datos.

- Crear una contraseña
    Para crear una contraseña se realiza una peticion POST y se le pedí al usuario por medio de las "Query Parameters" la información de la contraseña, la cual se almacena en la base de datos. Dicha informacion consta de:

    length (int): Longitud de la contraseña
    capital_letters (int): Cantidad de mayusculas de la contraseña
    numbers (int): Cantidad de numeros de la contraseña
    special_characters (int): Cantidad de caracteres especiales de la contraseña

    Con esta información se genera una contraseña aleatoria que cumpla con los requisitos del usuario.

-Actualizar una contraseña
    Para actualizar una contraseña se realiza una peticion PUT y se le pedí al usuario por medio de las "Query Parameters" la información de la contraseña, la cual se actualiza en la base de datos. Dicha informacion consta de:

    password_id (int):  Id de la contraseña a actualizar
    length (int): Longitud de la nueva contraseña
    capital_letters (int): Cantidad de mayusculas de la nueva contraseña
    numbers (int): Cantidad de numeros de la nueva contraseña
    special_characters (int): Cantidad de caracteres especiales de la nueva contraseña

    Con esta información se genera una contraseña aleatoria que cumpla con los requisitos del usuario.

- Eliminar una contraseña
    Para eliminar una contraseña se realiza una peticion DELETE y se le pedí al usuario por medio de las "Query Parameters" la información de la contraseña, la cual se elimina de la base de datos. Dicha informacion consta de:

    password_id (int): Id de la contraseña a eliminar

