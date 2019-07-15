from PortfolioWebsite import app
from flask import request, redirect
from waitress import serve

@app.before_request
def before_request():
    if not request.is_secure and app.env != "development":
        print(app.env)
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)

if __name__ == "__main__":
    serve(app, listen='*:80')
    # app.run(host='0.0.0.0', port='5000', debug=True)

