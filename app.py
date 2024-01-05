from flask import Flask, render_template

from apis.attraction import attraction
from apis.mrt import mrt
from apis.user import user
from apis.booking import booking
from apis.order import order
from models.db_connection import DB_Connector

app=Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["cnx_pool"] = DB_Connector() # 建立連線池

# Blueprints
app.register_blueprint(attraction)
app.register_blueprint(mrt)
app.register_blueprint(user)
app.register_blueprint(booking)
app.register_blueprint(order)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="0.0.0.0", port=3000)