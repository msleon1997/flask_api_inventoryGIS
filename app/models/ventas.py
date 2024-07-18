# API DE VENTAS

from flask import jsonify, request
from datetime import datetime
from decimal import Decimal
from app import app, conexion
import logging 
from flask import request, jsonify

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/ventas', methods=['POST'])
def registrarVentas():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        datos_ventas = {
            'VENT_codigo_venta': request.json.get('VENT_codigo_venta'),
            'cliente_id': request.json.get('cliente_id', ''),
            'producto_id': request.json.get('producto_id', None),
            'VENT_cantidad': request.json.get('VENT_cantidad', None),
            'VENT_producto_costo': request.json.get('VENT_producto_costo', ''),
            'VENT_total': request.json.get('VENT_total', None),
            'VENT_fecha_venta': date_added_default,
            'VENT_estado_venta': request.json.get('VENT_estado_venta'),
            'VENT_notas': request.json.get('VENT_notas', None),
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO tventas (VENT_codigo_venta, cliente_id, producto_id, VENT_cantidad, VENT_producto_costo, 
                VENT_total, VENT_fecha_venta, VENT_estado_venta, VENT_notas, users_id)
                 VALUES (%(VENT_codigo_venta)s, %(cliente_id)s, %(producto_id)s, %(VENT_cantidad)s, %(VENT_producto_costo)s, 
                        %(VENT_total)s, %(VENT_fecha_venta)s, %(VENT_estado_venta)s, %(VENT_notas)s, %(users_id)s)"""
        cursor.execute(sql, datos_ventas)
        conexion.connection.commit()
        return jsonify({'mensaje': "Venta registrada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/ventas/<id>', methods=['PUT'])
def actualizarVentas(id):
    try:
        venta = leerVenta(id)
        if venta is None:
            return jsonify({'mensaje': "Venta no encontrada.", 'exito': False})

        datos_ventas = {
            'VENT_codigo_venta': request.json.get('VENT_codigo_venta', venta['VENT_codigo_venta']),
            'cliente_id': request.json.get('cliente_id', venta['cliente_id']),
            'producto_id': request.json.get('producto_id', venta['producto_id']),
            'VENT_cantidad': request.json.get('VENT_cantidad', venta['VENT_cantidad']),
            'VENT_producto_costo': request.json.get('VENT_producto_costo', venta['VENT_producto_costo']),
            'VENT_total': request.json.get('VENT_total', venta['VENT_total']),
            'VENT_fecha_venta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'VENT_estado_venta': request.json.get('VENT_estado_venta', venta['VENT_estado_venta']),
            'VENT_notas': request.json.get('VENT_notas', venta['VENT_notas']),
            'users_id': request.json.get('users_id', venta['users_id']),
            'id': id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tventas SET VENT_codigo_venta = %(VENT_codigo_venta)s, cliente_id = %(cliente_id)s, 
                 producto_id = %(producto_id)s, VENT_cantidad = %(VENT_cantidad)s, VENT_producto_costo = %(VENT_producto_costo)s,
                 VENT_total = %(VENT_total)s, VENT_fecha_venta = %(VENT_fecha_venta)s, VENT_estado_venta = %(VENT_estado_venta)s,
                 VENT_notas = %(VENT_notas)s, users_id = %(users_id)s WHERE id = %(id)s"""
        cursor.execute(sql, datos_ventas)
        conexion.connection.commit()
        return jsonify({'mensaje': "Venta actualizada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/ventas', methods=['GET'])
def listarVentas():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT tv.id, tv.VENT_codigo_venta, tc.CLI_NombresCompletos AS cliente, pr.PRO_Nombre AS producto, tv.VENT_cantidad, pr.PRO_Precio AS VENT_producto_costo, 
                        tv.VENT_total, tv.VENT_fecha_venta, tv.VENT_estado_venta, tv.VENT_notas, tv.users_id 
                 FROM tventas tv
                 JOIN tcliente tc ON tv.cliente_id = tc.id 
                 JOIN tproducto pr ON tv.producto_id = pr.id"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        ventas = []
        for fila in datos:
            venta = {
                'id': fila[0],
                'VENT_codigo_venta': fila[1],
                'cliente': fila[2],
                'producto': fila[3],
                'VENT_cantidad': fila[4],
                'VENT_producto_costo': float(fila[5]),  # Convertir Decimal a float
                'VENT_total': float(fila[6]),  # Convertir Decimal a float
                'VENT_fecha_venta': fila[7].strftime('%Y-%m-%d %H:%M:%S') if isinstance(fila[7], datetime) else fila[7],
                'VENT_estado_venta': fila[8],
                'VENT_notas': fila[9],
                'users_id': fila[10]
            }
            ventas.append(venta)
        return jsonify({'ventas': ventas, 'mensaje': "Ventas listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})


@app.route('/api/ventas/<id>', methods=['GET'])
def leerVenta(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, VENT_codigo_venta, cliente_id, producto_id, VENT_cantidad, VENT_producto_costo, VENT_total, VENT_fecha_venta, VENT_estado_venta, VENT_notas, users_id FROM tventas WHERE id = %s"
        cursor.execute(sql, (id,))
        venta = cursor.fetchone()
        cursor.close()
        if venta:
            return {
                'id': venta[0],
                'VENT_codigo_venta': venta[1],
                'cliente_id': venta[2],
                'producto_id': venta[3],
                'VENT_cantidad': venta[4],
                'VENT_producto_costo': float(venta[5]),  # Convertir Decimal a float
                'VENT_total': float(venta[6]),  # Convertir Decimal a float
                'VENT_fecha_venta': venta[7].strftime('%Y-%m-%d %H:%M:%S') if isinstance(venta[7], datetime) else venta[7],
                'VENT_estado_venta': venta[8],
                'VENT_notas': venta[9],
                'users_id': venta[10]
            }
        else:
            return None
    except Exception as ex:
        return None

@app.route('/api/ventas/<id>', methods=['DELETE'])
def eliminarVenta(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tventas WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Venta eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Venta no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})