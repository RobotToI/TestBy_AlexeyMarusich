import sys
from typing import List
import requests

REQUEST_METHODS = {"GET": requests.get,
                    "OPTIONS": requests.options,
                    "HEAD": requests.head,
                    "POST": requests.post,
                    "PATCH": requests.patch,
                    "PUT": requests.put,
                    "DELETE": requests.delete
                    }


def get_info(url: str, avaliable_methods: List[str]):
    result = dict()
    for method in avaliable_methods:
        related_function = REQUEST_METHODS.get(method)
        status_code = related_function(url).status_code
        if status_code != 405:
            result[method] = status_code

    return result 


def validate_http_protocol_usage(url:str):
    if url.startswith('http://') or url.startswith('https://'):
        return True
    return False

def check_all_methods(url: str):
    verbs_avaliable = requests.options(url).headers.get('allow')
    if not verbs_avaliable:
        return {url: "No HTTP methods availiable"}
    avaliable_methods = verbs_avaliable.split(', ')
    result_responces = get_info(url, avaliable_methods)

    return {url: result_responces}


def read_lines_from_stdin():
    result_lines = set()
    for line in sys.stdin 
        if 'q' == line.rstrip().lower():
            break
        result_lines.add(line.rstrip())
        print(f"{line.rstrip()} has been taken to processing")
    print("Processing...\n")
    return result_lines

def main():
    urls = read_lines_from_stdin()
    output_json = dict()
    for url in urls:
        if validate_http_protocol_usage(url):
            output_json.update(check_all_methods(url))
        else:
            output_json.update({url: "Not valid url"})
    
    from pprint import pprint
    pprint(output_json)


if __name__ == "__main__":
    main()