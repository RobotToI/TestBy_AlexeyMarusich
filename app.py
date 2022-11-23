import sys
from typing import List

import requests
import validators


class MatchedRequests:
    __slots__ = "available_methods"

    _method_matching = {
        "GET": requests.get,
        "HEAD": requests.head,
        "POST": requests.post,
        "PATCH": requests.patch,
        "OPTIONS": requests.options,
        "DELETE": requests.delete,
    }

    def __init__(self, available_methods: List[str]):
        self.available_methods = [
            (k, value)
            for k, value in MatchedRequests._method_matching.items()
            if k in available_methods
        ]

    def __iter__(self):
        for method_name, method_function in self.available_methods:
            yield method_name, method_function
        return


class MethodResponseConfig:
    __slots__= 'url', 'available_methods'
    def __init__(self, url: str):
        self.url = url

    def get_method_responses(self):
        method_responses = dict()
        if not self.available_methods:
            return {self.url: "There is no available methods"}
        for method_name, method_function in MatchedRequests(self.available_methods):
            method_responses.update(
                {method_name: method_function(self.url).status_code}
            )

        return {self.url: method_responses}

    def set_available_methods(self):
        options_allows = requests.options(self.url).headers.get("allow")
        if not options_allows:
            self.available_methods = None
        else:
            self.available_methods = options_allows.split(", ")


def url_stdin_reader():
    """Function read lines from stdin and collects result in result set"""
    for line in sys.stdin:
        clear_line = line.rstrip().lower()
        if not clear_line:
            return
        if not validators.url(clear_line):
            continue
        yield clear_line


def main():
    result = list()
    for url in url_stdin_reader():
        config = MethodResponseConfig(url)
        config.set_available_methods()
        result.append(config.get_method_responses())
    from pprint import pprint

    pprint(result)


if __name__ == "__main__":
    main()
