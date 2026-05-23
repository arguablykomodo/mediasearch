import datetime
import argparse
import db

def search(args: argparse.Namespace):
    db.connect(args.directory)

    sort_method = db.File.mtime
    if args.sort == "date": sort_method = db.File.mtime
    elif args.sort == "match": sort_method = db.FileIndex.rank()
    if args.reverse: sort_method = -sort_method

    results = (db.FileIndex
        .select()
        .where(db.FileIndex.match(args.query))
        .join(db.File, on=(db.FileIndex.rowid == db.File.id))
        .order_by(sort_method))

    if args.limit: results = results.limit(args.limit)

    for result in results:
        print(result.path)

def index(args: argparse.Namespace):
    db.connect(args.directory)
    file_a = db.File.create(path="a.png", mtime=datetime.datetime.fromisoformat("2011-11-11"))
    file_b = db.File.create(path="b.png", text="The quick brown fox jumps over the lazy dog", mtime=datetime.datetime.fromisoformat("2003-11-11"))
    file_c = db.File.create(path="c.png", audio="Sphinx of black quartz, judge my vow", mtime=datetime.datetime.fromisoformat("2005-11-11"))
    file_d = db.File.create(path="d.png", text="The quick brown fox jumps over the lazy dog", audio="Sphinx of black quartz, judge my vow", mtime=datetime.datetime.fromisoformat("2018-11-11"))
    db.FileIndex.rebuild()
    db.FileIndex.optimize()

parser = argparse.ArgumentParser(
    prog="mediasearch",
    description="indexes and searches through media",
)
subparsers = parser.add_subparsers(required=True)

parser_search = subparsers.add_parser("search", help="Search for media")
_ = parser_search.add_argument("directory", type=str, help="Directory to search in")
_ = parser_search.add_argument("query", type=str, help="Search query")
_ = parser_search.add_argument("-s", "--sort", type=str, choices=["date", "match"], default="match", help="Sorting method (by modification date or by search match score)")
_ = parser_search.add_argument("--reverse", action="store_true", help="Reverse sort direction")
_ = parser_search.add_argument("-l", "--limit", type=int, help="Maximum number of results to output")
parser_search.set_defaults(func=search)

parser_index = subparsers.add_parser("index", help="Index a directory")
_ = parser_index.add_argument("directory", type=str, help="Directory to index")
parser_index.set_defaults(func=index)

args = parser.parse_args()
args.func(args)
