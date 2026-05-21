import argparse
import db

def search(args: argparse.Namespace):
    db.connect(args.directory)
    for file in db.File.select():
        print(file.id, file.path, file.text, file.audio)

def index(args: argparse.Namespace):
    db.connect(args.directory)
    file_a = db.File.create(path="a.png")
    file_b = db.File.create(path="b.png", text="The quick brown fox jumps over the lazy dog")
    file_c = db.File.create(path="c.png", audio="Sphinx of black quartz, judge my vow")
    file_d = db.File.create(path="d.png", text="The quick brown fox jumps over the lazy dog", audio="Sphinx of black quartz, judge my vow")

parser = argparse.ArgumentParser(
    prog="mediasearch",
    description="indexes and searches through media",
)
subparsers = parser.add_subparsers(required=True)

parser_search = subparsers.add_parser("search", help="Search for media")
_ = parser_search.add_argument("directory", type=str, help="Directory to search in")
_ = parser_search.add_argument("query", type=str, help="Search query")
parser_search.set_defaults(func=search)

parser_index = subparsers.add_parser("index", help="Index a directory")
_ = parser_index.add_argument("directory", type=str, help="Directory to index")
parser_index.set_defaults(func=index)

args = parser.parse_args()
args.func(args)
