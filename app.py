import uuid, json
from flask import Flask, render_template, redirect, url_for, request
from flask_uuid import FlaskUUID

app = Flask(__name__)
FlaskUUID(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_uuid/')
def create_uuid():
    with open('./static/urls.json', 'r+') as f:
        data = json.load(f)
        hashcode = str(uuid.uuid4())
        data[hashcode] = 0
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        return redirect(url_for('statistics', hashcode=hashcode))


@app.route('/tracky/<uuid(strict=False):hashcode>/counter/')
def counter(hashcode):
    return repr(hashcode)


@app.route('/tracky/<uuid(strict=False):hashcode>/statistics/')
def statistics(hashcode):
    with open('./static/urls.json', 'r') as f:
        data = json.load(f)
        return render_template('statistics.html', hashcode=hashcode, count=data[str(hashcode)])


if __name__ == '__main__':
    app.run(debug=True)
