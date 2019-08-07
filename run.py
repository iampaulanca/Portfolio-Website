from PortfolioWebsite import app, manager
from waitress import serve

if __name__ == "__main__":

    # For db migration (db init, db migrate, db upgrade)
    # manager.run()
    # For production
    serve(app, listen='0.0.0.0:80', url_scheme='https')
    # # For development
    # app.run(host='0.0.0.0', port=5000, debug=True)
