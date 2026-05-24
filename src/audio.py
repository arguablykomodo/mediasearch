import whisper

class Audio:
    model: whisper.Whisper

    def __init__(self):
        self.model = whisper.load_model("turbo")

    def parse(self, path: str, mimetype: tuple[str | None, str | None]):
        if mimetype[0] is not None and (mimetype[0].startswith("audio") or mimetype[0].startswith("video")):
            result = self.model.transcribe(path)
            return result["text"]
        else:
            return None
