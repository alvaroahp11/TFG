from flask import Blueprint, render_template, request, url_for, redirect
from .modelgenerator import modelgeneration
views = Blueprint('views', __name__)

prediction = ""
stock = ""
algoritmo = ""
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        global prediction
        global stock
        global algoritmo
        prediction = modelgeneration(request.form.to_dict(flat=False))
        stock = request.form["stock"]
        algoritmo = request.form["algorithm"]
        return redirect(url_for('views.result'))
    return render_template("base.html")

@views.route('/result')
def result():

    return render_template("result.html", resultado = prediction, accion = stock, algoritmo= algoritmo)
