from flask import jsonify, request
from datetime import datetime
from app import app, conexion
from app.validaciones import validar_cedula

@app.route('/api/users', methods=['POST'])
def registrar_usuario():
    try:
        cedula = request.json.get('cedula')
        if not validar_cedula(cedula):
            return jsonify({'mensaje': "Cédula inválida.", 'exito': False})

        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_updated_default = None

        datos_usuario = {
            'cedula': cedula,
            'firstname': request.json.get('firstname', ''),
            'middlename': request.json.get('middlename', None),
            'lastname': request.json.get('lastname', ''),
            'username': request.json.get('username', None),
            'password': request.json.get('password', ''),
            'avatar': request.json.get('avatar', None),
            'last_login': request.json.get('last_login', None),
            'type': request.json.get('type', None),
            'status': request.json.get('status', None),
            'date_added': date_added_default,
            'date_updated': date_updated_default
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO users (cedula, firstname, middlename, lastname, username, password, avatar, last_login, type, status, date_added, date_updated) 
                 VALUES (%(cedula)s, %(firstname)s, %(middlename)s, %(lastname)s, %(username)s, %(password)s, %(avatar)s, %(last_login)s, %(type)s, %(status)s, %(date_added)s, %(date_updated)s)"""
        cursor.execute(sql, datos_usuario)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/users/<id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        if not validar_cedula(id):
            return jsonify({'mensaje': "Cédula inválida.", 'exito': False})

        usuario = leer_usuario(id)

        if usuario is None:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})

        datos_usuario = {
            'cedula': request.json.get('cedula', usuario['cedula']),
            'firstname': request.json.get('firstname', usuario['firstname']),
            'middlename': request.json.get('middlename', usuario['middlename']),
            'lastname': request.json.get('lastname', usuario['lastname']),
            'username': request.json.get('username', usuario['username']),
            'password': request.json.get('password', usuario['password']),
            'avatar': request.json.get('avatar', usuario['avatar']),
            'last_login': request.json.get('last_login', usuario['last_login']),
            'type': request.json.get('type', usuario['type']),
            'status': request.json.get('status', usuario['status']),
            'date_added': usuario['date_added'],
            'date_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE users SET cedula = %(cedula)s, firstname = %(firstname)s, middlename = %(middlename)s, lastname = %(lastname)s,
                 username = %(username)s, password = %(password)s, avatar = %(avatar)s, last_login = %(last_login)s, type = %(type)s,
                 status = %(status)s, date_added = %(date_added)s, date_updated = %(date_updated)s 
                 WHERE id = %(id)s"""
        datos_usuario['id'] = id
        cursor.execute(sql, datos_usuario)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/users', methods=['GET'])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, firstname, middlename, lastname, username, password, avatar, last_login, type, status, date_added, date_updated FROM users"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            usuario = {
                'id': fila[0],
                'firstname': fila[1],
                'middlename': fila[2],
                'lastname': fila[3],
                'username': fila[4],
                'password': fila[5],
                'avatar': fila[6],
                'last_login': fila[7],
                'type': fila[8],
                'status': fila[9],
                'date_added': fila[10],
                'date_updated': fila[11]
            }
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/users/<id>', methods=['GET'])
def leer_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, firstname, middlename, lastname, username, password, avatar, last_login, type, status, date_added, date_updated FROM users WHERE id = %s"
        cursor.execute(sql, (id,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            return jsonify({
                'id': usuario[0],
                'firstname': usuario[1],
                'middlename': usuario[2],
                'lastname': usuario[3],
                'username': usuario[4],
                'password': usuario[5],
                'avatar': usuario[6],
                'last_login': usuario[7],
                'type': usuario[8],
                'status': usuario[9],
                'date_added': usuario[10],
                'date_updated': usuario[11],
                'mensaje': "Usuario encontrado.",
                'exito': True
            })
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/users/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM users WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
