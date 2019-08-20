from flask import Flask
from dash import Dash
import re
from django.http.response import HttpResponse
from bs4 import BeautifulSoup


URL_BASE_PATHNAME = '/dash/'+'dash_within_django/'

server = Flask(__name__)

app = Dash(server=server, url_base_pathname=URL_BASE_PATHNAME)

# if setting this app locally then some features may not display properly e.g. dropdown menus didnt display properly for me
# so I placed css content from the dash_core_components folder in dash_styles.css in static.
# on Windows, the css for other components can be found in e.g.:
#  C:\Users\{your_username}\AppData\Local\Continuum\anaconda3\Lib\site-packages\dash_core_components
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True


# this is called from views.py to get the response data from the Dash/Flask instance:
def dash_dispatcher(request,):
    '''
    Main function
    @param request: Request object
    '''

    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }

    with server.test_request_context(request.path, **params):
        server.preprocess_request()
        try:
            response = server.full_dispatch_request()
            # print('****', response)
        except Exception as e:
            response = server.make_response(server.handle_exception(e))
            # print('****EXCEPTION', response)
        return response.get_data()


def clean_dash_content(dash_content):
    ''' This is a hack to get rid of carriage returns in the html returned by the call to dash_dispatcher'''
    # print("Function: clean_dash_content")
    soup = BeautifulSoup(dash_content, 'lxml', from_encoding='utf-8')
    cleaned_dash_content = soup.body.decode_contents(formatter=None)
    return cleaned_dash_content
