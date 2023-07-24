from quopri import decodestring


class RequestProcessing:

    @staticmethod
    def get_method(environ, request):
        """
        the method read 'REQUEST_METHOD' from environ and returns request['method']  value
        @param environ:
        @param request:
        @return: request['method']
        """
        # print(f'Processing get_method')
        if environ['REQUEST_METHOD'] == 'GET':
            request['method'] = 'GET'
        elif environ['REQUEST_METHOD'] == 'POST':
            request['method'] = 'POST'
        else:
            raise ValueError('wrong request method')

    @staticmethod
    def process_get_request(environ, request):
        """
        The method reads binary string from environ , decodes it and parse it to dict
        @param environ:
        @param request:
        @return: request['data']
        """
        # print(f'process_get_request ')
        request['data'] = {}
        if 'QUERY_STRING' in environ and environ['QUERY_STRING']:
            request_data = environ['QUERY_STRING']
            request_list = request_data.split('&')
            param_dict_encoded = {}
            for r in request_list:
                k, v = r.split('=')
                param_dict_encoded[k] = v
            request['data'] = RequestProcessing.decode_value(param_dict_encoded)

    @staticmethod
    def process_post_request(environ, request):
        """
        The method requests binary string from environ , decodes it and parse it to dict
        @param environ:
        @param request:
        @return:  request['request_params']
        """
        request['request_params'] = {}
        encoded_data_string = RequestProcessing.get_wsgi_input_data(environ)     # got b'string'
        if encoded_data_string:
            data_string = encoded_data_string.decode(encoding='utf-8')
            data_list = data_string.split('&')
            encoded_data_dict = {}
            for r in data_list:
                k, v = r.split('=')
                encoded_data_dict[k] = v
            request['request_params'] = RequestProcessing.decode_value(encoded_data_dict)

    @staticmethod
    def decode_value(data: dict) -> dict:
        """
        The method decode bytestring and converts it to dict
        @param data: encoded dict
        @return: decoded dict
        """
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    @staticmethod
    def get_wsgi_input_data(environ: dict) -> bytes:
        """
        The method reads wsgi_data from environ for POST request
        @param environ:
        @return: bytes string
        """
        wsgi_data_length = environ.get('CONTENT_LENGTH')
        wsgi_data = b''
        if wsgi_data_length:
            wsgi_data_length = int(wsgi_data_length) if wsgi_data_length else 0
            wsgi_data = environ["wsgi.input"].read(wsgi_data_length)
        print(f'wsgi_data : {wsgi_data}')
        return wsgi_data







