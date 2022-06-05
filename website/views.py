from flask import Blueprint, render_template, request
from .modelgenerator import modelgeneration
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        modelgeneration(request.form.to_dict())
    return render_template("base.html")
