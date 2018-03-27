from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from .bib import find_published_entries

app = Flask(__name__)


def get_default_bibtext():
    with app.open_resource('default.bib', 'r') as f:
        bibtext = f.read()
    return bibtext


class BibForm(FlaskForm):
    bibtext = TextAreaField(
        'BibTeX file',
        validators=[DataRequired()],
        default=get_default_bibtext,
    )


@app.route('/', methods=['GET', 'POST'])
def main_view():
    form = BibForm(csrf_enabled=False)
    urls = None
    message = None
    if request.method == 'POST':
        if form.validate():
            bibtext = request.form['bibtext']
            urls = find_published_entries(bibtext, agent='arxiv_doi_updater')
        else:
            message = 'Wrong input!'
    return render_template('index.html', form=form, urls=urls, message=message)
