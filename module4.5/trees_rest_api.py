from flask import Flask, jsonify, abort
import requests

app = Flask(__name__)

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'

@app.route('/health/<string:health_id>', methods=['GET'])
def return_health(health_id):

    cap_health_id = health_id.capitalize()

    params = dict(
            health = cap_health_id
            )

    resp = requests.get(url=url, params=params)
    data = resp.json()

    return jsonify({"data": data})

@app.route('/zip/<int:zip_id>')
def return_zip(zip_id):
    params = dict(
            zipcode = zip_id
            )

    resp = requests.get(url=url, params=params)
    data = resp.json()

    return jsonify({"data": data})


if __name__ == '__main__':
    app.run(debug=True)
