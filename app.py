from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["DBLP"]
publis = db["publis"]

@app.route('/')
def list_publications():
    publications = publis.find({})
    return render_template('publications.html', publications=publications)

@app.route('/details/<publi_id>')
def show_details(publi_id):
    publication = publis.find_one({"_id": pymongo.ObjectId(publi_id)})
    return render_template('details.html', publication=publication)

@app.route('/filter', methods=['POST'])
def filter_publications():
    author = request.form['author']
    date = request.form['date']
    query = {}

    if author:
        query['authors'] = author

    if date:
        query['year'] = {'$gte': int(date)}

    publications = publis.find(query)
    return render_template('publications.html', publications=publications)


@app.route('/add_publication', methods=['POST'])
def add_publication():
    title = request.form['title']
    authors = request.form['authors'].split(',')
    year = int(request.form['year'])

    # Extract the author's name from the form
    author = request.form['author']

    publication_data = {
        'title': title,
        'authors': authors,
        'year': year,
        'author': author  # Include the author's name in the publication data
    }

    publis.insert_one(publication_data)
    return redirect('/')

@app.route('/result')
def show_result():
    # Affichez ici les résultats du filtrage
    return "Résultats du filtrage"

@app.route('/success')
def show_success():
    # Affichez ici un message de succès après l'ajout de la publication
    return "Publication ajoutée avec succès"

if __name__ == '__main__':
    app.run(debug=True)
