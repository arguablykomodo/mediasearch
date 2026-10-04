# `mediasearch`

`mediasearch` is a CLI program for indexing and searching through media
directories. The `index` command indexes all files in a given directory by
running OCR and speech recognition, storing the results in a searchable sqlite
database. The `search` command outputs a list of files maching the given search
terms given in [FTS query syntax][fqs].

[fqs]: https://sqlite.org/fts5.html#full_text_query_syntax

## Dependencies

- `peewee` for database ORM.
- `tqdm` for progress bars.
- `easyocr` for optical character recognition.
- `openai-whisper` for speech recognition.

## Building

The repo has a Nix flake for easy building and development. Otherwise, you can
use setuptools, or install the dependencies manually.

Building with CUDA support is heavily recommended.
