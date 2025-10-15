from flask import Flask, render_template, redirect, request, jsonify
from textblob import TextBlob

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def sentiment_analysis(paragraph):

    blob = TextBlob(paragraph)

    polarities =[]
    subjectivities =[]
    for sentences in blob.sentences:
        polarities.append(sentences.sentiment.polarity)
        subjectivities.append(sentences.sentiment.subjectivity)

    pol = sum(polarities)/len(polarities)
    subj = sum(subjectivities)/len(subjectivities)

    if pol > 0:
        sent = "Positive"
    elif pol < 0:
        sent = "Negative"
    else:
        sent = "Neutral"

    return pol, subj, sent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('textInput') or (request.json and request.json.get('textInput'))
    if not text:
        return jsonify({"error": "Please provide text to analyze."}), 400

    polarity, subjectivity, sentiment = sentiment_analysis(text)
    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity
    })

if __name__ == "__main__":
    app.run(debug=True)

