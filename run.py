from PortfolioWebsite import app
from waitress import serve


if __name__ == "__main__":

    # serve(app, listen='0.0.0.0:80', url_scheme='https')
    app.run(host='0.0.0.0', port=5000, debug=True)
