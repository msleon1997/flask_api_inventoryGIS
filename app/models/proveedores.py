from flask import jsonify, request
from datetime import datetime
from app import app, conexion
import logging 
from flask import request, jsonify



# Configuración básica de logging
logging.basicConfig(level=logging.INFO)


@app.route('/api/proveedores', methods=['POST'])
def registrarproveedores():
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        date_added_default = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        datos_proveedores = {
            'PROV_Identificacion': request.json.get('PROV_Identificacion'),
            'PROV_nombre_empresa': request.json.get('PROV_nombre_empresa'),
            'PROV_direccion': request.json.get('PROV_direccion'),
            'PROV_persona': request.json.get('PROV_persona'),
            'PROV_email': request.json.get('PROV_email'),
            'PROV_telefono': request.json.get('PROV_telefono'),
            'PROV_pagina_web': request.json.get('PROV_pagina_web', None),
            'PROV_fecha_registro': date_added_default,
            'notas': request.json.get('notas', None),
            'estado_proveedor': request.json.get('estado_proveedor'),
            'PM_Ciudad': request.json.get('PM_Ciudad'),
            'PM_Provincia': request.json.get('PM_Provincia'),
            'PM_Longitud': request.json.get('PM_Longitud'),
            'PM_Latitud': request.json.get('PM_Latitud'),
            'users_id':request.json.get('users_id')
            
        }

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO tproveedores (PROV_Identificacion, PROV_nombre_empresa, PROV_direccion, PROV_persona, PROV_email,
                      PROV_telefono, PROV_pagina_web, PROV_fecha_registro, notas, estado_proveedor, PM_Ciudad, PM_Provincia, PM_Longitud, PM_Latitud, users_id)
                      VALUES (%(PROV_Identificacion)s, %(PROV_nombre_empresa)s, %(PROV_direccion)s, %(PROV_persona)s, %(PROV_email)s, %(PROV_telefono)s,
                              %(PROV_pagina_web)s, %(PROV_fecha_registro)s, %(notas)s, %(estado_proveedor)s, %(PM_Ciudad)s, %(PM_Provincia)s, 
                              %(PM_Longitud)s, %(PM_Latitud)s, %(users_id)s)"""
        
        cursor.execute(sql, datos_proveedores)
        conexion.connection.commit()
        
        return jsonify({'message': 'Proveedor registrado', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito': False})

    

@app.route('/api/proveedores/<id>', methods = ['PUT'])
def actualizar_proveedores(id):
    try:
        datos_recibidos = request.json
        logging.info(f"Datos recibidos: {request.json}")
        proveedor = leer_proveedor(id)
        if proveedor is None:
            return jsonify({'mensaje': 'Proveedor no encontrado', 'exito':False})
        datos_proveedor = {

            'PROV_Identificacion': request.json.get('PROV_Identificacion', proveedor['PROV_Identificacion']),
            'PROV_nombre_empresa': request.json.get('PROV_nombre_empresa', proveedor['PROV_nombre_empresa']),
            'PROV_direccion': request.json.get('PROV_direccion', proveedor['PROV_direccion']),
            'PROV_persona': request.json.get('PROV_persona', proveedor['PROV_persona']),
            'PROV_email': request.json.get('PROV_email', proveedor['PROV_email']),
            'PROV_telefono': request.json.get('PROV_telefono', proveedor['PROV_telefono']),
            'PROV_pagina_web': request.json.get('PROV_pagina_web', proveedor['PROV_pagina_web']),
            'PROV_fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'notas': request.json.get('notas', proveedor['notas']),
            'estado_proveedor': request.json.get('estado_proveedor', proveedor['estado_proveedor']),
            'PM_Ciudad': request.json.get('PM_Ciudad', proveedor['PM_Ciudad']),
            'PM_Provincia': request.json.get('PM_Provincia', proveedor['PM_Provincia']),
            'PM_Longitud': request.json.get('PM_Longitud', proveedor['PM_Longitud']),
            'PM_Latitud': request.json.get('PM_Latitud', proveedor['PM_Latitud']),
            'users_id': request.json.get('users_id', proveedor['users_id']),
            'id' : id
        }

        cursor = conexion.connection.cursor()
        sql = """UPDATE tproveedores SET PROV_Identificacion = %(PROV_Identificacion)s, PROV_nombre_empresa = %(PROV_nombre_empresa)s, 
        PROV_direccion = %(PROV_direccion)s, PROV_persona = %(PROV_persona)s,
        PROV_email = %(PROV_email)s, PROV_telefono = %(PROV_telefono)s, PROV_pagina_web = %(PROV_pagina_web)s, 
        PROV_fecha_registro = %(PROV_fecha_registro)s, notas = %(notas)s, estado_proveedor = %(estado_proveedor)s, 
        PM_Ciudad = %(PM_Ciudad)s, PM_Provincia = %(PM_Provincia)s, PM_Longitud = %(PM_Longitud)s, 
        PM_Latitud = %(PM_Latitud)s, users_id = %(users_id)s where id = %(id)s"""

        cursor.execute(sql, datos_proveedor)
        conexion.connection.commit()
        return jsonify({'message': 'Proveedor actualizado', 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
    



@app.route('/api/proveedores', methods = ['GET'])
def listar_proveedores():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tproveedores"
        cursor.execute(sql)
        datosproveedores = cursor.fetchall()
        proveedores = []

        for fila in datosproveedores:
            proveedor = {
                'id': fila[0],
                'PROV_Identificacion': fila[1],
                'PROV_nombre_empresa': fila[2],
                'PROV_direccion': fila[3],
                'PROV_persona': fila[4],
                'PROV_email': fila[5],
                'PROV_telefono': fila[6],
                'PROV_pagina_web': fila[7],
                'PROV_fecha_registro': fila[8],
                'notas': fila[9],
                'estado_proveedor': fila[10],
                'PM_Ciudad': fila[11],
                'PM_Provincia': fila[12],
                'PM_Longitud': fila[13],
                'PM_Latitud': fila[14],
                'users_id': fila[15]
                
                
            }
            proveedores.append(proveedor)
        return jsonify({'proveedores': proveedores, 'mensaje': "Listado de Proveedores.", 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})
    


@app.route('/api/proveedores/<id>', methods = ['GET'])
def leer_proveedor(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM tproveedores WHERE id = %s"
        cursor.execute(sql, (id))
        proveedor = cursor.fetchone()
        cursor.close()
        if proveedor:
            return{
                'id': proveedor[0],
                'PROV_Identificacion': proveedor[1],
                'PROV_nombre_empresa': proveedor[2],
                'PROV_direccion': proveedor[3],
                'PROV_persona': proveedor[4],
                'PROV_email': proveedor[5],
                'PROV_telefono': proveedor[6],
                'PROV_pagina_web': proveedor[7],
                'PROV_fecha_registro': proveedor[8],
                'notas': proveedor[9],
                'estado_proveedor': proveedor[10],
                'PM_Ciudad': proveedor[11],
                'PM_Provincia': proveedor[12],
                'PM_Longitud': proveedor[13],
                'PM_Latitud': proveedor[14],
                'users_id': proveedor[15]
                
               
            }
        else:
            return None
    except Exception as ex:
            return None
    



@app.route('/api/proveedores/<id>', methods= ['DELETE'])
def eliminar_proveedor(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tproveedores WHERE id = %s"
        cursor.execute(sql, (id))
        conexion.connection.commit()

        if cursor.rowcount > 0:
            return jsonify({'mensaje': "Proveedor eliminado.", 'exito':True})
        else:
            return jsonify({'mensaje': "No se pudo eliminar el proveedor.", 'exito':False})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}", 'exito':False})