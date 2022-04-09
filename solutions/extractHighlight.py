import fitz

class extractHighlight():
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_annotation(self, annot, wordlist):
        points = annot.vertices
        quad_count = int(len(points) / 4)
        sentences = ['']*quad_count
        for i in range(quad_count):
            r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
            words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
            sentences[i] = ' '.join(w[4] for w in words)
        sentence = ' '.join(sentences)
        return sentence

    def extract_highlight_text_pdf(self):
        doc = fitz.open(self.filepath)
        highlights = []
        for page in doc:
            wordlist = page.get_text("words")
            wordlist = sorted(wordlist, key=lambda w: (w[3], w[0]))
            annot = page.firstAnnot
            while annot:
                if annot.type[0] == 8:
                    sentence = self.extract_annotation(annot, wordlist)
                    highlights.append(sentence)
                annot = annot.next
        return ' '.join(highlights)
