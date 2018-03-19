from flask import *
from csv import reader
from io import StringIO
from itertools import zip_longest

app = Flask(__name__)

def analyse(file):
    string_data = file.read().decode("utf-8")

    data = {'string_data': string_data}
    errors = ""
    try:
        rdr = reader(StringIO(string_data))
    except Exception as e:
        errors += f"{e}\n"

    try:
        rows = [row for row in rdr]
        data['rows'] = rows
    except Exception as e:
        errors += f"{e}\n"

    try:
        headings = list(zip_longest(rows[0][1:], (row[0] for row in rows[1:])))
        data['headings'] = headings
    except FileNotFoundError as e:
        errors += f"{e}\n"

    try:
        sum_weights = sum(sum((int(col) for col in row[1:] if col)) for row in rows[1:])
        data['sum_weights'] = sum_weights
    except Exception as e:
        errors += f"{e}\n"

    return render_template("result.html", data=data, errors=errors)



@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            return analyse(file)

    return "Something broke"


@app.route('/')
def hello_world():
    return render_template("input.html")


if __name__ == '__main__':
    app.run(debug=True)
