from flask import jsonify, request
from datetime import datetime
from app import app, conexion

@app.route('/api/prodrec', methods=['POST'])
def registrarProductoRecivido():
    try:
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        datos_productoRecivido = {
            'PRO_Nombre': request.json.get('PRO_Nombre'),
            'PRO_Descripcion': request.json.get('PRO_Descripcion', ''),
            'PRO_Precio': request.json.get('PRO_Precio', None),
            'PRO_ExcentoIva': request.json.get('PRO_ExcentoIva', None),
            'proveedor_id': request.json.get('proveedor_id', ''),
            'PRO_FechaCreacion': date_added_default,
            'PRO_Cantidad': request.json.get('PRO_Cantidad', None),
            'PRO_Estado': request.json.get('PRO_Estado', ''),
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO tproducto (PRO_Nombre, PRO_Descripcion, PRO_Precio, PRO_ExcentoIva, proveedor_id, 
                PRO_FechaCreacion, PRO_Cantidad, PRO_Estado, users_id)
                 VALUES (%(PRO_Nombre)s, %(PRO_Descripcion)s, %(PRO_Precio)s, %(PRO_ExcentoIva)s, %(proveedor_id)s, 
                         %(PRO_FechaCreacion)s, %(PRO_Cantidad)s, %(PRO_Estado)s, %(users_id)s)"""
        cursor.execute(sql, datos_productoRecivido)
        conexion.connection.commit()
        return jsonify({'mensaje': "Producto registrado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/prodrec/<id>', methods=['PUT'])
def actualizarProductoRecivido(id):
    try:
        datos_productoRecividos = {
            'PRO_Nombre': request.json.get('PRO_Nombre'),
            'PRO_Descripcion': request.json.get('PRO_Descripcion', ''),
            'PRO_Precio': request.json.get('PRO_Precio', None),
            'PRO_ExcentoIva': request.json.get('PRO_ExcentoIva', None),
            'proveedor_id': request.json.get('proveedor_id', ''),
            'PRO_FechaCreacion': request.json.get('PRO_FechaCreacion'),
            'PRO_Cantidad': request.json.get('PRO_Cantidad', None),
            'PRO_Estado': request.json.get('PRO_Estado', ''),
            'users_id': request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tproducto SET PRO_Nombre = %(PRO_Nombre)s, PRO_Descripcion = %(PRO_Descripcion)s, 
                 PRO_Precio = %(PRO_Precio)s, PRO_ExcentoIva = %(PRO_ExcentoIva)s, proveedor_id = %(proveedor_id)s, 
                 PRO_FechaCreacion = %(PRO_FechaCreacion)s, PRO_Cantidad = %(PRO_Cantidad)s, PRO_Estado = %(PRO_Estado)s, 
                 users_id = %(users_id)s WHERE id = %(id)s"""
        datos_productoRecividos['id'] = id
        cursor.execute(sql, datos_productoRecividos)
        conexion.connection.commit()
        return jsonify({'mensaje': "Producto actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/prodrec/<id>', methods=['GET'])
def leerProductoRecivido(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, PRO_Nombre, PRO_Descripcion, PRO_Precio, PRO_ExcentoIva, proveedor_id, PRO_FechaCreacion, PRO_Cantidad, PRO_Estado, users_id FROM tproducto WHERE id = %s"
        cursor.execute(sql, (id,))
        producto = cursor.fetchone()
        cursor.close()
        if producto:
            return jsonify({
                'id': producto[0],
                'PRO_Nombre': producto[1],
                'PRO_Descripcion': producto[2],
                'PRO_Precio': float(producto[3]),
                'PRO_ExcentoIva': producto[4],
                'proveedor_id': producto[5],
                'PRO_FechaCreacion': producto[6],
                'PRO_Cantidad': producto[7],
                'PRO_Estado': producto[8],
                'users_id': producto[9]
            })
        else:
            return jsonify({'mensaje': "Producto no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/prodrec', methods=['GET'])
def leerProductosRecividos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, PRO_Nombre, PRO_Descripcion, PRO_Precio, PRO_ExcentoIva, proveedor_id, PRO_FechaCreacion, PRO_Cantidad, PRO_Estado, users_id FROM tproducto"
        cursor.execute(sql)
        productos = cursor.fetchall()
        cursor.close()
        resultado = []
        for producto in productos:
            resultado.append({
                'id': producto[0],
                'PRO_Nombre': producto[1],
                'PRO_Descripcion': producto[2],
                'PRO_Precio': float(producto[3]),
                'PRO_ExcentoIva': producto[4],
                'proveedor_id': producto[5],
                'PRO_FechaCreacion': producto[6],
                'PRO_Cantidad': producto[7],
                'PRO_Estado': producto[8],
                'users_id': producto[9]
            })
        return jsonify(resultado)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

@app.route('/api/prodrec/<id>', methods=['DELETE'])
def eliminarProductoRecivido(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tproducto WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Producto eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Producto no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})