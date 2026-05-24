import easyocr

class Text:
    reader: easyocr.Reader

    def __init__(self, langs: list[str]):
        self.reader = easyocr.Reader(langs)

    def parse(self, path: str, mimetype: tuple[str | None, str | None]):
        if mimetype[0] is not None and mimetype[0].startswith("image"):
            paragraphs = self.reader.readtext(path, detail=0, paragraph=True)
            return " ".join(paragraphs)
        else:
            return None
