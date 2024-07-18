from flask import jsonify, logging, request
from datetime import datetime
from app import app, conexion
import logging 
from flask import request, jsonify

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/devoluciones', methods=['POST'])
def registrarDevoluciones():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        datos_devoluciones = {
            'DEV_codigo_devolucion': request.json.get('DEV_codigo_devolucion'),
            'DEV_unidad': request.json.get('DEV_unidad', ''),
            'DEV_cantidad_devuelta': request.json.get('DEV_cantidad_devuelta', 0),
            'DEV_producto_costo': request.json.get('DEV_producto_costo', 0.0),
            'DEV_total_devolucion': request.json.get('DEV_total_devolucion', 0.0),
            'DEV_fecha_devolucion': date_added_default,
            'DEV_razon_devolucion': request.json.get('DEV_razon_devolucion', ''),
            'DEV_estado_devolucion': request.json.get('DEV_estado_devolucion', 'Activo'),
            'DEV_notas': request.json.get('DEV_notas', ''),
            'proveedor_id': request.json.get('proveedor_id'),
            'producto_id': request.json.get('producto_id'),
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO tdevoluciones (DEV_codigo_devolucion, DEV_unidad, DEV_cantidad_devuelta, DEV_producto_costo, DEV_total_devolucion, DEV_fecha_devolucion, DEV_razon_devolucion, DEV_estado_devolucion, DEV_notas, proveedor_id, producto_id, users_id)
                 VALUES (%(DEV_codigo_devolucion)s, %(DEV_unidad)s, %(DEV_cantidad_devuelta)s, %(DEV_producto_costo)s, %(DEV_total_devolucion)s, %(DEV_fecha_devolucion)s, %(DEV_razon_devolucion)s, %(DEV_estado_devolucion)s, %(DEV_notas)s, %(proveedor_id)s, %(producto_id)s, %(users_id)s)"""
        cursor.execute(sql, datos_devoluciones)
        conexion.connection.commit()
        
        return jsonify({'mensaje': "Devolución registrada.", 'exito': True})
    except Exception as ex:
        logging.error(f"Error al registrar devolución: {str(ex)}")
        return jsonify({"error": "Hubo un error al procesar la solicitud"}), 500

@app.route('/api/devoluciones/<id>', methods=['PUT'])
def actualizarDevoluciones(id):
    try:
        
        devolucion = leerDevoluciones(id)
        if devolucion is None:
            return jsonify({'mensaje': "Devolución no encontrada.", 'exito': False})

        datos_devoluciones = {
            'DEV_codigo_devolucion': request.json.get('DEV_codigo_devolucion', devolucion['DEV_codigo_devolucion']),
            'DEV_unidad': request.json.get('DEV_unidad', devolucion['DEV_unidad']),
            'DEV_cantidad_devuelta': request.json.get('DEV_cantidad_devuelta', devolucion['DEV_cantidad_devuelta']),
            'DEV_producto_costo': request.json.get('DEV_producto_costo', devolucion['DEV_producto_costo']),
            'DEV_total_devolucion': request.json.get('DEV_total_devolucion', devolucion['DEV_total_devolucion']),
            'DEV_fecha_devolucion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'DEV_razon_devolucion': request.json.get('DEV_razon_devolucion', devolucion['DEV_razon_devolucion']),
            'DEV_estado_devolucion': request.json.get('DEV_estado_devolucion', devolucion['DEV_estado_devolucion']),
            'DEV_notas': request.json.get('DEV_notas', devolucion['DEV_notas']),
            'proveedor_id': request.json.get('proveedor_id', devolucion['proveedor_id']),
            'producto_id': request.json.get('producto_id', devolucion['producto_id']),
            'users_id': request.json.get('users_id', devolucion['users_id']),
            'id': id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tdevoluciones SET DEV_codigo_devolucion = %(DEV_codigo_devolucion)s, DEV_unidad = %(DEV_unidad)s, DEV_cantidad_devuelta = %(DEV_cantidad_devuelta)s, DEV_producto_costo = %(DEV_producto_costo)s, DEV_total_devolucion = %(DEV_total_devolucion)s,
                 DEV_fecha_devolucion = %(DEV_fecha_devolucion)s, DEV_razon_devolucion = %(DEV_razon_devolucion)s, DEV_estado_devolucion = %(DEV_estado_devolucion)s, DEV_notas = %(DEV_notas)s, proveedor_id = %(proveedor_id)s, producto_id = %(producto_id)s, users_id = %(users_id)s
                 WHERE id = %(id)s"""
        cursor.execute(sql, datos_devoluciones)
        conexion.connection.commit()
        return jsonify({'mensaje': "Devolución actualizada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})


@app.route('/api/devoluciones', methods=['GET'])
def listarDevoluciones():
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT d.id, d.DEV_codigo_devolucion, d.DEV_unidad, d.DEV_cantidad_devuelta, d.DEV_producto_costo, 
                   d.DEV_total_devolucion, d.DEV_fecha_devolucion, d.DEV_razon_devolucion, d.DEV_estado_devolucion, 
                   d.DEV_notas, p.PROV_persona AS proveedor_nombre, pr.PRO_Nombre AS producto_nombre, d.users_id
            FROM tdevoluciones d
            JOIN tproveedores p ON d.proveedor_id = p.id
            JOIN tproducto pr ON d.producto_id = pr.id
        """
        cursor.execute(sql)
        datos = cursor.fetchall()
        devoluciones = []
        for fila in datos:
            devolucion = {
                'id': fila[0],
                'DEV_codigo_devolucion': fila[1],
                'DEV_unidad': fila[2],
                'DEV_cantidad_devuelta': fila[3],
                'DEV_producto_costo': float(fila[4]),  # Convertir Decimal a float
                'DEV_total_devolucion': float(fila[5]),  # Convertir Decimal a float
                'DEV_fecha_devolucion': fila[6],
                'DEV_razon_devolucion': fila[7],
                'DEV_estado_devolucion': fila[8],
                'DEV_notas': fila[9],
                'proveedor_nombre': fila[10],  # Nombre del proveedor
                'producto_nombre': fila[11],   # Nombre del producto
                'users_id': fila[12]
            }
            devoluciones.append(devolucion)
        return jsonify({'devoluciones': devoluciones, 'mensaje': "Devoluciones listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})




@app.route('/api/devoluciones/<id>', methods=['GET'])
def leerDevoluciones(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, DEV_codigo_devolucion, DEV_unidad, DEV_cantidad_devuelta, DEV_producto_costo, DEV_total_devolucion, DEV_fecha_devolucion, DEV_razon_devolucion, DEV_estado_devolucion, DEV_notas, proveedor_id, producto_id, users_id FROM tdevoluciones WHERE id = %s"
        cursor.execute(sql, (id,))
        devolucion = cursor.fetchone()
        cursor.close()
        if devolucion:
            return {
                'id': devolucion[0],
                'DEV_codigo_devolucion': devolucion[1],
                'DEV_unidad': devolucion[2],
                'DEV_cantidad_devuelta': devolucion[3],
                'DEV_producto_costo': float(devolucion[4]),  # Convertir Decimal a float
                'DEV_total_devolucion': float(devolucion[5]),  # Convertir Decimal a float
                'DEV_fecha_devolucion': devolucion[6],
                'DEV_razon_devolucion': devolucion[7],
                'DEV_estado_devolucion': devolucion[8],
                'DEV_notas': devolucion[9],
                'proveedor_id': devolucion[10],
                'producto_id': devolucion[11],
                'users_id': devolucion[12]
            }
        else:
            return None
    except Exception as ex:
        return None

@app.route('/api/devoluciones/<id>', methods=['DELETE'])
def eliminarDevoluciones(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tdevoluciones WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Devolución eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Devolución no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})