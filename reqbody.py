from urllib.parse import urlparse, parse_qs
import json
def convert_docid(docid):
    # Replace underscores with dots
    docid = docid.replace('_', '.')
    
    # Replace hyphens with dots
    docid = docid.replace('-', '.')
    
    # Split the string by dots and exclude the last part
    parts = docid.split('.')
    docid = '.'.join(parts[:-1])
    
    return docid


def generate_request_body(url):
    # Parse the URL
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    # # Extract relevant information
    city = path_parts[0]
    search = path_parts[1]
    docid=convert_docid(path_parts[2])
    
    
    # # Parse the query parameters
    query_params = parse_qs(parsed_url.query)
    ncatid = query_params.get('ncatid', [''])[0]
    catname = query_params.get('mncatname', [''])[0]
    
    # Construct the body
    body = {
        "city": city,
        "search": search,
        "docid": docid,
        "ncatid": ncatid,
        "catname": catname,
        "mobile": "",
        "bid": 0,
        "pdid": None,
        "search_id": "",
        "trkid": "",
        "useTabsView": True
    }
    body_json = json.dumps(body, indent=4)
    return body_json


