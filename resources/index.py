from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint("Index",__name__,description="Index page to link to the documentation")

@blp.route("/")
class Index(MethodView):
    def get(self):
        html = "<!DOCTYPE html><html><head><style>body{background-color:white;text-align:center;padding-top:5%;font-family: Arial, Helvetica, sans-serif;}</style><title>Flask Store API - DocLinks</title></head><body><h1>This is a Flask Store API</h1><p>Documentation can be found <a href='/swagger-ui' target='blank'>here<a></p></body></html>"
        return html