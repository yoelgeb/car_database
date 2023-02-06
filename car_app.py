from flask import Flask, jsonify, request, render_template
from car_database_queries import CarQuery

app = Flask(__name__)

car_data = CarQuery()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/cars", methods=["GET","POST"])
def handle_create_read():
    if (request.method == "GET"):
        return jsonify(car_data.read_data().to_dict(orient="records"))
    if request.method == "POST":
        data = request.get_json()
        car_data.add_car(data)
        return "Car Added."

@app.route("/cars/<id>", methods=["GET", "PUT", "DELETE"])
def handle_update_delete(id):
    try:
        int_id = int(id)
    except ValueError:
        return "ID must be an int"
    if request.method == "GET":
        return car_data.read_data_id(int_id).to_dict()
    if request.method == "PUT":
        data = request.get_json()
        car_data.update_car(data, int_id)
        return "Car Updated"
    if request.method == "DELETE":
        car_data.remove_cars("StockID", int_id)
        return "Car Deleted"

if __name__ == "__main__":
    app.run(port=8080)












if __name__ == "__main__":
    app.run(port=8080)