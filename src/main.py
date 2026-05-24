from datetime import datetime
import argparse
import db
import os

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
    filepaths = next(os.walk(args.directory), (None, None, []))[2] # https://stackoverflow.com/a/3207973
    for filepath in filepaths:
        mtime = datetime.fromtimestamp(os.stat(filepath).st_mtime)
        file, created = db.File.get_or_create(path=filepath, defaults={"mtime": mtime})
        if file.mtime > mtime or created or args.force:
            file.mtime = mtime
    db.File.delete().where(db.File.path.not_in(filepaths))
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
    _ = parser_search.add_argument("-f", "--force", action="store_true", help="Re-index already indexed files")
    parser_index.set_defaults(func=index)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
