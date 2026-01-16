from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def analyze():
    sentiment = None
    polarity = 0
    subjectivity = 0
    polarity_percent = 0
    subjectivity_percent = 0

    if request.method == "POST":
        text = request.form.get("text_analysis", "")

        review = TextBlob(text)
        polarity = review.sentiment.polarity
        subjectivity = review.sentiment.subjectivity

        # sentiment label
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # convert to meter percentages
        polarity_percent = int((polarity + 1) / 2 * 100)   # -1..1 → 0..100
        subjectivity_percent = int(subjectivity * 100)     # 0..1 → 0..100

    return render_template(
        "index.html",
        sentiment=sentiment,
        polarity=round(polarity, 2),
        subjectivity=round(subjectivity, 2),
        polarity_percent=polarity_percent,
        subjectivity_percent=subjectivity_percent
    )

if __name__ == "__main__":
    app.run(debug=True)
