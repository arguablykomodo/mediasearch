import argparse

def search(args: argparse.Namespace):
    print("Search unimplemented")
    print("args:", args)
    pass

def index(args: argparse.Namespace):
    print("Indexing unimplemented")
    print("args:", args)
    pass

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
