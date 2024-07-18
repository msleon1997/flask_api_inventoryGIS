from flask import jsonify, request
from datetime import datetime
from app import app, conexion
import logging 
from flask import request, jsonify


# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/clientes', methods=['POST'])
def registrar_clientes():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Procesar el nombre completo recibido desde el formulario
        nombre_completo = request.json.get('CLI_NombreCompleto', '')
        nombres = nombre_completo.split() if nombre_completo else []
        
        datos_clientes = {
            'CLI_Identificacion': request.json['CLI_Identificacion'],
            'CLI_TipoIdentificacion': request.json['CLI_TipoIdentificacion'],
            'CLI_NombresCompletos': request.json['CLI_NombresCompletos'],
            'CLI_Direccion': request.json['CLI_Direccion'],
            'CLI_Telefono': request.json['CLI_Telefono'],
            'CLI_Correo': request.json['CLI_Correo'],
            'CLI_FechaNacimiento': request.json['CLI_FechaNacimiento'],
            'CLI_FechaCreacion': date_added_default,
            'users_id': request.json['users_id']
        }

        cursor = conexion.connection.cursor()

        sql = """INSERT INTO tcliente (CLI_Identificacion, CLI_TipoIdentificacion, CLI_NombresCompletos, CLI_Direccion, CLI_Telefono, CLI_Correo, CLI_FechaNacimiento, CLI_FechaCreacion, users_id)
        VALUES (%(CLI_Identificacion)s, %(CLI_TipoIdentificacion)s, %(CLI_NombresCompletos)s, %(CLI_Direccion)s, %(CLI_Telefono)s, %(CLI_Correo)s, %(CLI_FechaNacimiento)s,
        %(CLI_FechaCreacion)s, %(users_id)s)"""
        
        cursor.execute(sql, datos_clientes)
        conexion.connection.commit()
        
        return jsonify({'message': 'Cliente registrado', 'exito':True})
    except Exception as ex:
        logging.error(f"Error al registrar devolución: {str(ex)}")
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})

@app.route('/api/clientes/<id>', methods=['PUT'])
def actualizar_clientes(id):
    try:
        cliente = leer_cliente(id)
        if cliente is None:
            return jsonify({'mensaje': 'Cliente no encontrado', 'exito':False})
        
        datos_cliente = {
            'CLI_Identificacion': request.json.get('CLI_Identificacion', cliente['CLI_Identificacion']),
            'CLI_TipoIdentificacion': request.json.get('CLI_TipoIdentificacion', cliente['CLI_TipoIdentificacion']),
            'CLI_NombresCompletos': request.json.get('CLI_NombresCompletos', cliente['CLI_NombresCompletos']),
            'CLI_Direccion': request.json.get('CLI_Direccion', cliente['CLI_Direccion']),
            'CLI_Telefono': request.json.get('CLI_Telefono', cliente['CLI_Telefono']),
            'CLI_Correo': request.json.get('CLI_Correo', cliente['CLI_Correo']),
            'CLI_FechaNacimiento': request.json.get('CLI_FechaNacimiento', cliente['CLI_FechaNacimiento']),
            'CLI_FechaCreacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'users_id': request.json.get('users_id', cliente['users_id'])
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tcliente SET CLI_Identificacion = %(CLI_Identificacion)s, CLI_TipoIdentificacion = %(CLI_TipoIdentificacion)s,
        CLI_NombresCompletos = %(CLI_NombresCompletos)s, CLI_Direccion = %(CLI_Direccion)s, CLI_Telefono = %(CLI_Telefono)s, CLI_Correo = %(CLI_Correo)s,
        CLI_FechaNacimiento = %(CLI_FechaNacimiento)s, CLI_FechaCreacion = %(CLI_FechaCreacion)s, users_id = %(users_id)s where id = %(id)s"""
        cursor.execute(sql, {**datos_cliente, 'id': id})
        conexion.connection.commit()
        
        return jsonify({'message': 'Cliente actualizado', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tcliente"
        cursor.execute(sql)
        datosclientes = cursor.fetchall()
        clientes = []

        for fila in datosclientes:
            cliente = {
                'id': fila[0],
                'CLI_Identificacion': fila[1],
                'CLI_TipoIdentificacion': fila[2],
                'CLI_NombresCompletos': fila[3],
                'CLI_Direccion': fila[4],
                'CLI_Telefono': fila[5],
                'CLI_Correo': fila[6],
                'CLI_FechaNacimiento': fila[7],
                'CLI_FechaCreacion': fila[8],
                'users_id': fila[9]
            }
            clientes.append(cliente)
        return jsonify({'clientes': clientes, 'mensaje': "Listado de Clientes.", 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})

@app.route('/api/clientes/<id>', methods=['GET'])
def leer_cliente(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tcliente WHERE id = %s"
        cursor.execute(sql, (id,))
        cliente = cursor.fetchone()
        cursor.close()
        if cliente:
            return {
                'id': cliente[0],
                'CLI_Identificacion': cliente[1],
                'CLI_TipoIdentificacion': cliente[2],
                'CLI_NombresCompletos': cliente[3],
                'CLI_Direccion': cliente[4],
                'CLI_Telefono': cliente[5],
                'CLI_Correo': cliente[6],
                'CLI_FechaNacimiento': cliente[7],
                'CLI_FechaCreacion': cliente[8],
                'users_id': cliente[9]
            }
        else:
            return None
    except Exception as ex:
        return None

@app.route('/api/clientes/<id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tcliente WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Cliente eliminado.", 'exito':True})
        else:
            return jsonify({'mensaje': "No se pudo eliminar el cliente.", 'exito':False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
