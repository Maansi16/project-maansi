from flask import Flask, render_template, request
import os
from ranker import process_and_rank

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("resumes")
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        ranked_resumes = process_and_rank()
        return render_template("index.html", resumes=ranked_resumes)
    return render_template("index.html", resumes=None)
@app.route('/rank', methods=['POST'])
def rank():
    # Get uploaded resumes
    resumes = request.files.getlist('resumes')
    job_desc = request.form['job_description']
 


    # (Your NLP and ranking logic will go here)
    # For now, just return confirmation
    return f"<h2>{len(resumes)} resume(s) uploaded.</h2><p>Job Description received: {job_desc[:100]}...</p>"

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
