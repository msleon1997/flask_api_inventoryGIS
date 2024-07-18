from flask import jsonify, request
from datetime import datetime
from decimal import Decimal
from app import app, conexion
import logging 
from flask import request, jsonify


# Configuración básica de logging
logging.basicConfig(level=logging.INFO)


@app.route('/api/ordenes', methods=['POST'])
def registrarOrdenes():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       

        datos_ordenes = {
            'codigo_compra': request.json.get('codigo_compra'),
            'cantidad': request.json.get('cantidad', None),
            'precio': request.json.get('precio', ''),
            'impuesto': request.json.get('impuesto', None),
            'descuento': request.json.get('descuento', None),
            'total': request.json.get('total', None),
            'observaciones': request.json.get('observaciones', None),
            'fecha_creacion': date_added_default,
            'estado': request.json.get('estado'),
            'proveedores_id': request.json.get('proveedores_id'),
            'producto_id': request.json.get('producto_id'),
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO ordenes_compra (codigo_compra, cantidad, precio, impuesto, 
                descuento, total, observaciones, fecha_creacion, estado, proveedores_id, producto_id, users_id)
                 VALUES (%(codigo_compra)s, %(cantidad)s, %(precio)s, %(impuesto)s, 
                        %(descuento)s, %(total)s, %(observaciones)s, %(fecha_creacion)s, %(estado)s, %(proveedores_id)s, %(producto_id)s, %(users_id)s)"""
        cursor.execute(sql, datos_ordenes)
        conexion.connection.commit()
        return jsonify({'mensaje': "Orden de compra registrada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
    


@app.route('/api/ordenes/<id>', methods=['PUT'])
def actualizar_ordenes(id):
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        orden = leer_ordenes(id)
        if orden is None:
            return jsonify({'mensaje': "Orden de compra no encontrada.", 'exito': False})

        datos_ordenes = {
            'codigo_compra': request.json.get('codigo_compra', orden['codigo_compra']),
            'cantidad': request.json.get('cantidad', orden['cantidad']),
            'precio': request.json.get('precio', orden['precio']),
            'impuesto': request.json.get('impuesto', orden['impuesto']),
            'descuento': request.json.get('descuento', orden['descuento']),
            'total': request.json.get('total', orden['total']),
            'observaciones': request.json.get('observaciones', orden['observaciones']),
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'estado': request.json.get('estado', orden['estado']),
            'users_id': request.json.get('users_id', orden['users_id']),
            'proveedores_id': request.json.get('proveedores_id', orden['proveedores_id']),
            'producto_id': request.json.get('producto_id', orden['producto_id']),
            'id': id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE ordenes_compra SET codigo_compra = %(codigo_compra)s,
                 cantidad = %(cantidad)s, precio = %(precio)s, impuesto = %(impuesto)s, descuento = %(descuento)s, total = %(total)s,
                 observaciones = %(observaciones)s, fecha_creacion = %(fecha_creacion)s, estado = %(estado)s, proveedores_id = %(proveedores_id)s, producto_id = %(producto_id)s , users_id = %(users_id)s
                 WHERE id = %(id)s"""
        cursor.execute(sql, datos_ordenes)
        conexion.connection.commit()
        return jsonify({'mensaje': "Orden de compra actualizada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})





@app.route('/api/ordenes', methods=['GET'])
def listar_ordenes():
    try:
        cursor = conexion.connection.cursor()
        sql = """ SELECT o.id, o.codigo_compra,
                   o.cantidad, o.precio, o.impuesto, o.descuento, 
                   o.total, o.observaciones, o.fecha_creacion, o.estado, p.PROV_persona AS proveedor, pr.PRO_Nombre AS producto, o.users_id
            FROM ordenes_compra o
            JOIN tproveedores p ON o.proveedores_id = p.id
            JOIN tproducto pr ON o.producto_id = pr.id """
        cursor.execute(sql)
        datos = cursor.fetchall()
        ordenes = []
        for fila in datos:
            orden = {
                'id': fila[0],
                'codigo_compra': fila[1],
                'cantidad': fila[2],
                'precio': float(fila[3]),  # Convertir Decimal a float
                'impuesto': float(fila[4]) if fila[7] is not None else None,  # Convertir Decimal a float
                'descuento': float(fila[5]) if fila[8] is not None else None,  # Convertir Decimal a float
                'total': float(fila[6]),  # Convertir Decimal a float
                'observaciones': fila[7],
                'fecha_creacion': fila[8],
                'estado': fila[9],
                'proveedor': fila[10],
                'producto' : fila[11],
                'users_id': fila[12]
            }
            ordenes.append(orden)
        return jsonify({'ordenes': ordenes, 'mensaje': "Ordenes de compra listadas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})


    

@app.route('/api/ordenes/<id>', methods=['GET'])
def leer_ordenes(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, codigo_compra, cantidad, precio, impuesto, descuento, total, observaciones, fecha_creacion, estado, users_id, proveedores_id, producto_id  FROM ordenes_compra WHERE id = %s"
        cursor.execute(sql, (id,))
        orden = cursor.fetchone()
        cursor.close()
        if orden:
            return {
                'id': orden[0],
                'codigo_compra': orden[1],
                'cantidad': orden[2],
                'precio': float(orden[3]),  # Convertir Decimal a float
                'impuesto': float(orden[4]) if orden[7] is not None else None,  # Convertir Decimal a float
                'descuento': float(orden[5]) if orden[8] is not None else None,  # Convertir Decimal a float
                'total': float(orden[6]),  # Convertir Decimal a float
                'observaciones': orden[7],
                'fecha_creacion': orden[8],
                'estado': orden[9],
                'users_id': orden[10],
                'proveedores_id' : orden[11],
                'producto_id' : orden[12]

            }
        else:
            return None
    except Exception as ex:
        return None

    




@app.route('/api/ordenes/<id>', methods=['DELETE'])
def eliminar_ordenes(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM ordenes_compra WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Orden de compra eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Orden de compra no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})
