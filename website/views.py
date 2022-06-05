from flask import Blueprint, render_template, request
from .modelgenerator import modelgeneration
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    # modelgeneration(request.form.to_dict(flat=False))
    return render_template("base.html")
