from flask import Flask, render_template, request
from redis import Redis
from rq import Queue
from worker import conn
from clipper import process_clip
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "devsecret")
q = Queue(connection=conn)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clip", methods=["POST"])
def clip():
    youtube_url = request.form.get("youtube_url")
    if youtube_url:
        job = q.enqueue(process_clip, youtube_url)
        return f"Job queued! ID: {job.id}"
    return "No URL provided!"

if __name__ == "__main__":
    app.run(debug=True)