from flask import jsonify, request
from datetime import datetime
from app import app, conexion

@app.route('/api/proveedoresMap', methods=['POST'])
def registrarProveedoresMap():
    try:

        datos_proveedoresMap = {
            'PM_Ciudad': request.json.get('PM_Ciudad'),
            'PM_Provincia': request.json.get('PM_Provincia'),
            'PM_Longitud': request.json.get('PM_Longitud'),
            'PM_Latitud': request.json.get('PM_Latitud'),
            'users_id':request.json.get('users_id')
        }

        cursor = conexion.connection.cursor()

        sql = """INSERT INTO tproveedoresmap (PM_Ciudad, PM_Provincia, PM_Longitud, PM_Latitud, users_id)
        values(%(PM_Ciudad)s, %(PM_Provincia)s, %(PM_Longitud)s, %(PM_Latitud)s, %(users_id)s)"""
        
        cursor.execute(sql, datos_proveedoresMap)
        conexion.connection.commit()
        
        return jsonify({'message': 'Proveedor registrado', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
    

@app.route('/api/proveedoresMap/<id>', methods = ['PUT'])
def actualizar_proveedoresMap(id):
    try:
        proveedorMap = leer_proveedorMap(id)
        if proveedorMap is None:
            return jsonify({'mensaje': 'Proveedor no encontrado', 'exito':False})
        datos_proveedoresMap = {

            'PM_Ciudad': request.json.get('PM_Ciudad', proveedorMap['PM_Ciudad']),
            'PM_Provincia': request.json.get('PM_Provincia', proveedorMap['PM_Provincia']),
            'PM_Longitud': request.json.get('PM_Longitud', proveedorMap['PM_Longitud']),
            'PM_Latitud': request.json.get('PM_Latitud', proveedorMap['PM_Latitud']),
            'users_id': request.json.get('users_id', proveedorMap['users_id']),
            'id' : id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tproveedoresmap SET PM_Ciudad = %(PM_Ciudad)s, PM_Provincia = %(PM_Provincia)s, PM_Longitud = %(PM_Longitud)s, PM_Latitud = %(PM_Latitud)s,
         users_id = %(users_id)s where id = %(id)s"""
        cursor.execute(sql, datos_proveedoresMap)
        conexion.connection.commit()
        return jsonify({'message': 'Proveedor actualizado', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
    


@app.route('/api/proveedoresMap', methods = ['GET'])
def listar_proveedoresMap():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tproveedoresmap"
        cursor.execute(sql)
        datosproveedoresMap = cursor.fetchall()
        proveedoresMap = []

        for fila in datosproveedoresMap:
            proveedorMap = {
                'id': fila[0],
                'PM_Ciudad': fila[1],
                'PM_Provincia': fila[2],
                'PM_Longitud': fila[3],
                'PM_Latitud': fila[4],
                'users_id': fila[5]
            }
            proveedoresMap.append(proveedorMap)
        return jsonify({'proveedores': proveedoresMap, 'mensaje': "Listado de proveedores en mapa.", 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})


@app.route('/api/proveedoresMap/<id>', methods = ['GET'])
def leer_proveedorMap(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tproveedoresmap WHERE id = %s"
        cursor.execute(sql, (id))
        proveedorMap = cursor.fetchone()
        cursor.close()
        if proveedorMap:
            return{
                'id': proveedorMap[0],
                'PM_Ciudad': proveedorMap[1],
                'PM_Provincia': proveedorMap[2],
                'PM_Longitud': proveedorMap[3],
                'PM_Latitud': proveedorMap[4],
                'users_id': proveedorMap[5]
            }
        else:
            return None
    except Exception as ex:
            return None

@app.route('/api/proveedoresMap/<id>', methods= ['DELETE'])
def eliminar_proveedorMap(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tproveedoresmap WHERE id = %s"
        cursor.execute(sql, (id))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Proveedor eliminado del mapa.", 'exito':True})
        else:
            return jsonify({'mensaje': "No se pudo eliminar el proveedor del mapa.", 'exito':False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})