from flask import jsonify, logging, request
from datetime import datetime
from app import app, conexion
import logging 
from flask import request, jsonify


# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/productos', methods=['POST'])
def registrarProducto():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_defualt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        datos_productos = {
            'PRO_Nombre': request.json.get('PRO_Nombre'),
            'PRO_Descripcion':request.json.get('PRO_Descripcion'),
            'PRO_Precio':request.json.get('PRO_Precio'),
            'PRO_ExcentoIva':request.json.get('PRO_ExcentoIva'),
            'PRO_FechaCreacion':date_added_defualt,
            'PRO_Cantidad':request.json.get('PRO_Cantidad'),
            'PRO_Total': request.json.get('PRO_Total'),
            'PRO_Estado':request.json.get('PRO_Estado'),
            'users_id':request.json.get('users_id'),
            'proveedor_id':request.json.get('proveedor_id')
           
        }

        cursor = conexion.connection.cursor()

        sql = """INSERT INTO tproducto  (PRO_Nombre,PRO_Descripcion,PRO_Precio,proveedor_id,PRO_FechaCreacion
        ,PRO_Cantidad,PRO_Total,PRO_Estado,users_id) VALUES (%(PRO_Nombre)s,%(PRO_Descripcion)s,%(PRO_Precio)s,%(proveedor_id)s,
        %(PRO_FechaCreacion)s,%(PRO_Cantidad)s,%(PRO_Total)s,%(PRO_Estado)s,%(users_id)s)"""

        cursor.execute(sql, datos_productos)
        conexion.connection.commit()

        return jsonify({'mensaje':'Se ha registrado correctamente el producto.', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
    



@app.route('/api/productos/<id>', methods=['PUT'])
def actualizar_Producto(id):
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        producto = leer_producto(id)
        if producto is None:
            return jsonify({'mensaje': 'No se ha encontrado el producto.', 'exito':False})
        
        # Verificar que proveedor_id esté presente en los datos recibidos
        if 'proveedor_id' not in datos_recibidos:
            return jsonify({'mensaje': 'El campo proveedor_id es requerido.', 'exito': False})

        datos_producto = {
            'PRO_Nombre': datos_recibidos.get('PRO_Nombre', producto['PRO_Nombre']),
            'PRO_Descripcion': datos_recibidos.get('PRO_Descripcion', producto['PRO_Descripcion']),
            'PRO_Precio': datos_recibidos.get('PRO_Precio', producto['PRO_Precio']),
            'PRO_ExcentoIva': datos_recibidos.get('PRO_ExcentoIva', producto['PRO_ExcentoIva']),
            'PRO_FechaCreacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'PRO_Cantidad': datos_recibidos.get('PRO_Cantidad', producto['PRO_Cantidad']),
            'PRO_Total': datos_recibidos.get('PRO_Total', producto['PRO_Total']),
            'PRO_Estado': datos_recibidos.get('PRO_Estado', producto['PRO_Estado']),
            'users_id': datos_recibidos.get('users_id', producto['users_id']),
            'proveedor_id': datos_recibidos.get('proveedor_id', producto['proveedor_id']),
            'id': id
        }
    
        cursor = conexion.connection.cursor()
        sql = """UPDATE tproducto SET PRO_Nombre = %(PRO_Nombre)s, PRO_Descripcion = %(PRO_Descripcion)s, PRO_Precio = %(PRO_Precio)s, PRO_ExcentoIva = %(PRO_ExcentoIva)s,
                    PRO_FechaCreacion = %(PRO_FechaCreacion)s, PRO_Cantidad = %(PRO_Cantidad)s , PRO_Total = %(PRO_Total)s, PRO_Estado = %(PRO_Estado)s, users_id = %(users_id)s,  proveedor_id = %(proveedor_id)s WHERE id = %(id)s"""
        cursor.execute(sql, datos_producto)
        conexion.connection.commit()
        return jsonify({'mensaje': 'Producto actualizado correctamente.', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})




    
@app.route('/api/productos', methods=['GET'])
def listar_productos():
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





@app.route('/api/productos/<id>', methods = ['GET'])
def leer_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT p.id, p.PRO_Nombre, p.PRO_Descripcion, p.PRO_Precio, p.PRO_ExcentoIva, p.PRO_FechaCreacion, 
                        p.PRO_Cantidad, p.PRO_Total, p.PRO_Estado, p.users_id, p.proveedor_id, pr.PROV_persona 
                 FROM tproducto p 
                 JOIN tproveedores pr ON p.proveedor_id = pr.id 
                 WHERE p.id = %s"""
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
        cursor.close()
        if producto:
            return{
                'id': producto[0],
                'PRO_Nombre': producto[1],
                'PRO_Descripcion': producto[2],
                'PRO_Precio': float(producto[3]),
                'PRO_ExcentoIva': producto[4],
                'PRO_FechaCreacion': producto[5],
                'PRO_Cantidad': producto[6],
                'PRO_Total': float(producto[7]),
                'PRO_Estado': producto[8],
                'users_id': producto[9],
                'proveedor_id': producto[10],
                'PROV_persona': producto[11],
                
            }
        else:
            return None
    except Exception as ex:
        return None





@app.route('/api/productos/<id>', methods = ['DELETE'])
def eliminar_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tproducto WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': 'Producto eliminado correctamente.', 'exito':True})
        else:
            return jsonify({'mensaje': 'No se pudo eliminar el producto.', 'exito':False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})