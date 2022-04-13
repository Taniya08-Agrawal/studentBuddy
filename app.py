from solutions.extractHighlight import extractHighlight
from solutions.tfidf import tfidf
from solutions.abstractive import abstractive

from flask import *
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        filename = f.filename
        if not filename[-3:].lower() == 'pdf':
            os.remove(filename)
            return render_template("index.html", error = "Unsupported file format. Only pdf format allowed!")
        if request.form['type']=="highlighted":
            try:
                highlight_model = extractHighlight(filename)
                highlighted_text = highlight_model.extract_highlight_text_pdf()
                
                if len(highlighted_text) == 0:
                    os.remove(filename)
                    return render_template("index.html", error = "Highlighted text not found.")
                
                extractive_model = tfidf(highlighted_text)
                ext_summary = extractive_model.extractive_summarization()
                abstractive_model = abstractive(ext_summary)
                summary = abstractive_model.abstractive_summarization()
                
                os.remove(filename)
                return render_template("index.html", f_text = summary)
            except:
                return render_template("index.html", error = "Sorry! Unable to generate summary.")
        
        else:
            try:
                page_range = request.form['kind']
                page_range_list = page_range.split('-')
                start = int(page_range_list[0].strip())
                end = int(page_range_list[1].strip())
                
                extractive_model = tfidf(filename, start, end)
                ext_summary = extractive_model.extractive_summarization()
                abstractive_model = abstractive(ext_summary)
                summary = abstractive_model.abstractive_summarization()
                
                os.remove(filename)
                return render_template("index.html", f_text = summary)
            except:
                return render_template("index.html", error = "Sorry! Unable to generate summary.")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)      