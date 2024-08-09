import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='dpg-cqoc76rv2p9s73anf3jg-a.oregon-postgres.render.com',
                            database='dbflask',
                            user='dbflask_user',
                            password='ANhEPfhFkIHcTaAdvQwRkTr6FrIlwGJI')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM movies;')
    movies = [] 
    moviesFet = cur.fetchall()
    cur.close()
    conn.close()
    
    """
    HTML (<li>) de todos os dados.
    """
    html = ""
    
    for row in moviesFet:
        movies.append({"name": row[0], "rating": row[1]})
    
    for movie in movies:
    
        html = html + """
            <li class="list-group-item">
                <span class="badge">%s
                    <span class="glyphicon glyphicon-star"></span>
                </span>
                %s
            </li>
        """ % (movie['rating'], movie['name'])
       
    return open('index.html').read()  % (html)

@app.route('/novo_filme', methods=['POST'])
def novo_filme():
    if request.method == 'POST':
        titulo = request.form['titulo_filme']
        nota = request.form['nota']

        # Conectar ao banco de dados e inserir os dados
        conn = get_db_connection()
        conn.execute('INSERT INTO movies (name, rating) VALUES (?, ?)',
                     (titulo, nota))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)