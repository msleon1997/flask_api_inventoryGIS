from flask import jsonify, request
from datetime import datetime
from decimal import Decimal
from app import app, conexion
import logging 
from flask import request, jsonify


# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/categorias', methods=['POST'])
def registrarCategoria():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       

        datos_categoriass = {
            'CAT_Nombre': request.json.get('CAT_Nombre'),
            'CAT_Fecha': date_added_default,
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO categorias_productos (CAT_Nombre, CAT_Fecha, users_id)
                 VALUES (%(CAT_Nombre)s, %(CAT_Fecha)s, %(users_id)s)"""
        cursor.execute(sql, datos_categoriass)
        conexion.connection.commit()
        return jsonify({'mensaje': "Categoria creada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
    


@app.route('/api/categorias/<id>', methods=['PUT'])
def actualizar_categorias(id):
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        orden = leer_categorias(id)
        if orden is None:
            return jsonify({'mensaje': "Orden de compra no encontrada.", 'exito': False})

        datos_categorias = {
            'CAT_Nombre': request.json.get('CAT_Nombre', orden['CAT_Nombre']),
            'CAT_Fecha': request.json.get('CAT_Fecha', orden['CAT_Fecha']),
            'users_id': request.json.get('users_id', orden['users_id']),
            'id': id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE categorias_productos SET CAT_Nombre = %(CAT_Nombre)s, CAT_Fecha = %(CAT_Fecha)s, users_id = %(users_id)s WHERE id = %(id)s"""
        cursor.execute(sql, datos_categorias)
        conexion.connection.commit()
        return jsonify({'mensaje': "Categoria actualizada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})



@app.route('/api/categorias', methods=['GET'])
def listar_categorias():
    try:
        cursor = conexion.connection.cursor()
        sql = " SELECT id, CAT_Nombre, CAT_Fecha, users_id FROM categorias_productos "
        cursor.execute(sql)
        datos = cursor.fetchall()
        categorias = []
        for fila in datos:
            categoria = {
                'id': fila[0],
                'CAT_Nombre': fila[1],
                'CAT_Fecha': fila[2],
                'users_id': fila[3]
            }
            categorias.append(categoria)
        return jsonify({'categorias': categorias, 'mensaje': "Categorias listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
    

@app.route('/api/categorias/<id>', methods=['GET'])
def leer_categorias(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, CAT_Nombre, CAT_Fecha, users_id FROM categorias_productos WHERE id = %s"
        cursor.execute(sql, (id,))
        categoria = cursor.fetchone()
        cursor.close()
        if categoria:
            return {
                'id': categoria[0],
                'CAT_Nombre': categoria[1],
                'CAT_Fecha': categoria[2],
                'users_id': categoria[3]

            }
        else:
            return None
    except Exception as ex:
        return None

    

@app.route('/api/categorias/<id>', methods=['DELETE'])
def eliminar_categorias(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM categorias_productos WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Categoria eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Categoria no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
