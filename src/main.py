from datetime import datetime
import argparse
import mimetypes
from tqdm import tqdm
import os
import sys
import db
from text import Text

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
    files = next(os.walk(args.directory), (None, None, []))[2] # https://stackoverflow.com/a/3207973

    if args.types is None:
        args.types = ["text", "audio"]
    text = None
    if "text" in args.types:
        if args.lang is None:
            raise Exception("No languages were specified")
        text = Text(args.lang)

    for name in tqdm(files):
        filepath = os.path.realpath(os.path.join(args.directory, name))
        mtime = datetime.fromtimestamp(os.stat(filepath).st_mtime)
        mimetype = mimetypes.guess_file_type(filepath)
        file, created = db.File.get_or_create(path=filepath, defaults={"mtime": mtime})
        if file.mtime > mtime or created or args.force:
            file.mtime = mtime
            if text is not None:
                try:
                    file.text = text.parse(filepath, mimetype)
                except Exception as e:
                    print(f"\033[31mError during text recognition for file {filepath}:\033[39m {e}", file=sys.stderr)
            file.save()
    db.File.delete().where(db.File.path.not_in(files))
    db.FileIndex.rebuild()
    db.FileIndex.optimize()

def main():
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
    _ = parser_index.add_argument("-f", "--force", action="store_true", help="Re-index already indexed files")
    _ = parser_index.add_argument("-t", "--text", dest="types", action="append_const", const="text", help="Only run optical character recognition")
    _ = parser_index.add_argument("-a", "--audio", dest="types", action="append_const", const="audio", help="Only run speech recognition")
    _ = parser_index.add_argument("-l", "--lang", action="append", help="Language to recognize (as ISO language code), multiple allowed")
    parser_index.set_defaults(func=index)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
