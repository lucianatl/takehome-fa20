from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

""""
f minRating is provided as a query string parameter, only return the restaurants which have that rating or above. If there are no such restaurants, return a 404 with a descriptive message.

For this exercise, you can ignore any query string parameters other than minRating and you may assume that the provided parameter will be an integer represented as a string of digits.

In Postman, you can supply query string parameters writing the query string into your request url or by hitting the Params button next to Send. Doing so will automatically fill in the request url.

"""
@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})

@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/restaurants", methods=['GET'])
def get_all_restaurants():
    restaurants = db.get('restaurants')
    minRating = request.args.get('minRating')
    filtered_restuarants = []

    #check to see if there is a minRating param
    if minRating is None:
      return create_response({"restaurants": db.get('restaurants')})
    
    for restaurant in restaurants:
        if restaurant['rating'] >= int(minRating):
          filtered_restuarants.append(restaurant)

    # if nothing is rated equal to or higher than minRating, return an error
    if not filtered_restuarants:
      return create_response(status=404, message="there are no restaurants that match your minimum rating")

    return create_response({"restaurants": filtered_restuarants})
    

@app.route("/restaurants/<id>", methods=['GET'])
def get_restaurant(id):
  restaurant = db.getById('restaurants', int(id))
  return create_response(restaurant)

@app.route("/restaurants/<id>", methods=['DELETE'])
def delete_restaurant(id):
    if db.getById('restaurants', int(id)) is None:
        return create_response(status=404, message="No restaurant with this id exists")
    db.deleteById('restaurants', int(id))
    return create_response(message="Restaurant deleted")


# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
