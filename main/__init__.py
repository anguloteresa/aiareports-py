from flask import Flask
import azure.functions as func



app = Flask(__name__)

# code for azure funcs
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

# code for flask

@app.route('/api/test')
def test():
    return "<p>Hello, World!</p>"