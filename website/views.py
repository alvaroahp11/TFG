from flask import Blueprint, render_template, request, url_for, redirect
from .modelgenerator import modelgeneration
views = Blueprint('views', __name__)

prediction = ""

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        global prediction
        prediction = modelgeneration(request.form.to_dict(flat=False))
        return redirect(url_for('views.result'))
    return render_template("base.html")

@views.route('/result')
def result():

    return render_template("result.html", resultado = prediction)
