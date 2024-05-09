from flask import Flask, jsonify, request
from flask_mysqldb import MySQL


from config import config



app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos', methods=['GET'])
def listar_cursos():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT Codigo, Nombre, Creditos FROM curso"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso={'codigo':fila[0], 'nombre':fila[1], 'creditos':fila[2]}
            cursos.append(curso)
        return jsonify({'cursos':cursos, 'mensaje':"Cursos Listados"})
    except Exception as ex:
        return jsonify({'mensaje':"error"})
    

@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT Codigo, Nombre, Creditos FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            curso={'codigo':datos[0], 'nombre':datos[1], 'creditos':datos[2]}
            return jsonify({'cursos':curso, 'mensaje':"Cursos Listados"})
        else:
            return jsonify({'cursos':"curso no encontrado"})

    except Exception as ex:
        return jsonify({'mensaje':"error"})    
    
@app.route('/cursos', methods=['POST'])
def registrar_curso():
    try:
        #print(request.json)
        cursor=conexion.connection.cursor()
        sql="SELECT Codigo FROM curso"
        cursor.execute(sql)
        codigos=cursor.fetchall()
        for fila in codigos:
            codigo = fila[0]
            if codigo == request.json['codigo']: 
                codigo_repetido = True
                break
            else:
                codigo_repetido = False
        if codigo_repetido == False:
            cursor=conexion.connection.cursor()
            sql="INSERT INTO curso (Codigo, Nombre, Creditos) VALUES ('{0}','{1}','{2}')".format(request.json['codigo'],request.json['nombre'],request.json['creditos'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"curso registrado"})
        else:
            return jsonify({'mensaje':"curso ya antes registrado"})

    except Exception as ex:
        return jsonify({'mensaje':"error"})
    

@app.route('/curso/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM curso WHERE Codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"curso Eliminado"})
    except Exception as ex:
        return jsonify({'mensaje':"error"}) 

def page_not_found(error):
    return "<h1>La pagina solicitada no existe</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()