from flask import Flask, request, render_template
import os
import requests

"""
to run the app, do
flask --app flaskr run
or in pycharm:
-edit configuration
-set Target type to 'Module name'
-set Target to 'flaskr'
"""

def create_app(test_config=None):
    app = Flask(__name__)

    opendata_link = "https://open.tan.fr"

    if test_config:
        app.config.update({
            "TESTING": True,
        })

    @app.route('/')
    def hello_world():
        return render_template('index.html')


    # Recherche arrets proche d'une latitude/longitude
    @app.route('/find_arret/<latitude>/<longitude>', methods=['GET'])
    def get_closest_arret(latitude, longitude):
        req = requests.get(opendata_link + "/ewp/arrets.json/{latitude}/{longitude}").json()
        return req


    # Liste de tous les arrets

    @app.route('/arrets', methods=['GET','POST'])
    def get_arrets_by_ligne():
        arrets = requests.get(opendata_link + '/ewp/arrets.json').json()
        if request.method == 'POST':
            # Retrieve the text from the textarea
            num_ligne = request.form.get('textarea')
            # Print the text in terminal for verification
            arrets_ligne = []
            for arret in arrets:
                if {"numLigne": num_ligne} in arret['ligne']:
                    arrets_ligne.append(arret)
            return render_template('arrets.jinja2', arrets=arrets_ligne)
        return render_template('arrets.jinja2', arrets=arrets)


    # Horaires (théoriques)

    # Temps Attente

    # Temps attente pour un lieu ou arret et un nombre de passages

    # Temps attente pour un lieu ou arret, un nombre de passages et un numéro de ligne

    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host='0.0.0.0', port=port)