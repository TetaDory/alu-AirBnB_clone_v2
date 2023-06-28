#!/usr/bin/python3
"""simple flask routes"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states():
    """return html for filter"""
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    sorted_list = sorted(states, key=lambda x: x['name'])
    for i in sorted_list:
        cities = [d for d in cities if d['state_id'] == i['id']]
        i['cities'] = sorted(cities, key=lambda x: x['name'])
    return render_template('10-hbnb_filter.html',
                           states=sorted_list, amenities=amenities)


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
