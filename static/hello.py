from cgi import parse_qs

def application(environ, start_response):
    status = '200 OK'
    output = 'Hello world WSGI'
    request = environ['QUERY_STRING']
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            size_of = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            size_of = 0
        request = environ['wsgi.input'].read(size_of)
    output += environ['REQUEST_METHOD']
    d = parse_qs(request)
    for i in d.keys():
        output = output + " \n " + i + " = " + d.get(i,[''])[0]
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
