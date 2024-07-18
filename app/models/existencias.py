from flask import jsonify, logging, request
from datetime import datetime
from app import app, conexion
import logging 
from flask import request, jsonify

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/existencias', methods=['GET'])
def listar_existencias():
    try:
        cursor = conexion.connection.cursor()
        sql = """ SELECT p.id, p.PRO_Nombre, p.PRO_Descripcion, p.PRO_Precio, p.PRO_ExcentoIva, 
                         p.PRO_FechaCreacion, p.PRO_Cantidad, p.PRO_Total, p.PRO_Estado, p.users_id, pr.PROV_persona AS proveedor_nombre
                  FROM tproducto p 
                  JOIN tproveedores pr ON p.proveedor_id = pr.id """
        cursor.execute(sql)
        datos = cursor.fetchall()
        productos = []

        for fila in datos:
            producto = {
                'id': fila[0],
                'PRO_Nombre': fila[1],
                'PRO_Descripcion': fila[2],
                'PRO_Precio': float(fila[3]),
                'PRO_ExcentoIva': fila[4],
                'PRO_FechaCreacion': fila[5],
                'PRO_Cantidad': fila[6],
                'PRO_Total': float(fila[7]),
                'PRO_Estado': fila[8],
                'users_id': fila[9],
                'proveedor_nombre': fila[10]
            }
            productos.append(producto)
        return jsonify({'productos': productos, 'mensaje': "Listado de Productos.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})