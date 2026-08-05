from flask import Flask, render_template #Creacion de la aplicacion

app = Flask(__name__) 

@app.route('/') # la pagina principal direcciona a la raiz
def index():
    return render_template('index.html') # mostrar el html

if __name__== '__main__': 
    app.run(debug=True) # inicia el servidor
    