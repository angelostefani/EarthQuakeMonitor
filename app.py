import csv
from io import StringIO
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Pagina principale
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filters = {
            'starttime': request.form['starttime'],
            'endtime': request.form['endtime'],
            'minlat': request.form['minlat'],
            'maxlat': request.form['maxlat'],
            'minlon': request.form['minlon'],
            'maxlon': request.form['maxlon'],
            'lat': request.form['lat'],
            'lon': request.form['lon'],
            'minradius': request.form['minradius'],
            'maxradius': request.form['maxradius'],
            'minradiuskm': request.form['minradiuskm'],
            'maxradiuskm': request.form['maxradiuskm'],
            'minmag': request.form['minmag'],
            'maxmag': request.form['maxmag'],
            'mindepth': request.form['mindepth'],
            'maxdepth': request.form['maxdepth'],
            'eventid': request.form['eventid'],
            'format': 'text'
        }
        # Rimuovi i parametri vuoti o non valorizzati
        filters = {k: v for k, v in filters.items() if v}
        earthquakes = get_earthquakes(filters)
        return render_template('index.html', earthquakes=earthquakes)
    return render_template('index.html', earthquakes=None)

# Funzione per ottenere i terremoti utilizzando il servizio REST dell'INGV
def get_earthquakes(filters):
    url = 'https://webservices.ingv.it/fdsnws/event/1/query' 
    response = requests.get(url, params=filters)
    if response.status_code == 200:
        try:
            response_text = response.text
            # Utilizza csv.reader per leggere il file CSV
            csv_data = csv.reader(StringIO(response_text), delimiter='|')
            
            # Salta la prima riga contenente gli header
            next(csv_data)
            
            # Inizializza la lista di terremoti
            earthquakes = []
            for row in csv_data:
                earthquake = {
                    'EventID': row[0],
                    'Time': row[1],
                    'Latitude': row[2],
                    'Longitude': row[3],
                    'Depth/Km': row[4],
                    'MagType': row[9],
                    'Magnitude': row[10],
                    'EventLocationName': row[12],
                    'EventType': row[13]
                }
                earthquakes.append(earthquake)
            return earthquakes
        except Exception as e:
            print(e)  # Gestisci l'errore, ad esempio loggandolo
            return None
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
