
# importing all the required libaries and modules
from flask import Flask, render_template, request
import google.auth
from google.cloud import translate

# creating a flask
app = Flask(__name__)

# fetching the GCP project id
_, PROJECT_ID = google.auth.default()

# creating a GCP translation service client
TRANSLATE = translate.TranslationServiceClient()
PARENT = 'projects/{}'.format(PROJECT_ID)

# Creating a source and target language to translate variables
# We will be converting english to French
SOURCE, TARGET = ('en', 'English'), ('fr', 'French')

# Creating a "get and post" route for flask server
# Translate function
@app.route('/', methods=['GET', 'POST'])
def translate(gcf_request=None):

    #request object to be passed in GCP
    local_request = gcf_request if gcf_request else request

    # Resetting all the variables for get requests
    text = translated = None

    # proceed if the request method is post
    if local_request.method == 'POST':
        text = local_request.form['text'].strip()
        if text:
            data = {
                'contents': [text],
                'parent': PARENT,
                'target_language_code': TARGET[0],
            }
            try:
                rsp = TRANSLATE.translate_text(request=data)
            except TypeError:
                rsp = TRANSLATE.translate_text(**data)
            translated = rsp.translations[0].translated_text

    context = {
        'orig':  {'text': text, 'lc': SOURCE},
        'trans': {'text': translated, 'lc': TARGET},
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    import os
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
