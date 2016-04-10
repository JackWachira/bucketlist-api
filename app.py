"""Import statements."""
from resources.endpoints import app

if __name__ == '__main__':
    app.debug = True
    # run the flask app
    app.run(debug=True)
