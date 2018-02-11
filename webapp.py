import logging
import os
import pickle

from flask import Flask, render_template, request, g, redirect, url_for

from form import QueryForm
from labeler import LabelWriter, ImageReaderSolr

app = Flask(__name__)
app.config.from_object('config.settings')


def save_reader(reader):
    with open(app.config.get('READER'), mode='wb') as f:
        pickle.dump(reader, f)


def get_reader():
    reader_pickle_name = app.config.get('READER')
    if os.path.isfile(reader_pickle_name):
        with open(reader_pickle_name, mode='rb') as file:
            return pickle.load(file)


@app.before_request
def init_reader():
    g.reader = get_reader()


@app.before_request
def init_writer():
    g.writer = LabelWriter()


@app.route('/search', methods=['GET', 'POST'])
def search():
    query_form = QueryForm()
    if query_form.validate_on_submit():
        g.reader = ImageReaderSolr(query_form.query.data)

        save_reader(g.reader)

        return redirect(url_for('label'))

    for error in query_form.errors:
        print(error)

    return render_template('search.html', query_form=query_form)


@app.route('/label', methods=['GET', 'POST'])
def label_image():
    image_url = None

    # TODO change request to POST to not get confused
    if request.args.get('label') and request.args.get('url'):
        g.writer.write(request.args.get('url'), request.args.get('label'))

    next_image = g.reader.next()

    # persist
    save_reader(g.reader)

    if next_image:
        image_url = next_image.split(' ')[0]

    return render_template('labeling.html', image_url=image_url)


if __name__ == '__main__':
    logging.basicConfig(filename='labeler.log', level=logging.INFO)
    app.run(debug=True)
