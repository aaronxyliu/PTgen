from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import json


with open('data/DetectFile.json', 'r') as openfile:
    file_list = json.load(openfile)


## Page Template Language (PTL) Reference:
##    Chamelon language reference: chameleon.readthedocs.io/en/latest/reference.html
##    Blog: majornetwork.net/2021/03/templating-your-python-output-with-chameleon
@view_config(route_name='lib_test', renderer='test_page.pt')
def lib_testing(request):
    index = str(request.matchdict['file_index'])

    file_info = file_list[index]
    lib_list = file_info['out_deps'][:]
    lib_list.append(file_info['url'])
    return dict(libname = file_info['libname'], 
                filename = file_info['filename'],
                version = file_info['version'],
                libs = lib_list)

@view_config(route_name='only_deps', renderer='test_page.pt')
def dep_testing(request):
    index = str(request.matchdict['file_index'])
    
    file_info = file_list[index]
    lib_list = file_info['out_deps'] + file_info['in_deps']
    return dict(libname = file_info['libname'], 
                filename = file_info['filename'],
                version = file_info['version'],
                libs = lib_list)




if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('lib_test', '/test/{file_index}')
        config.add_route('only_deps', '/deps/{file_index}')
        
        config.include('pyramid_chameleon')

        config.scan('app')
        config.add_static_view(name='static', path='static')
        app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    server.serve_forever()


# 127.0.0.1:6543/test/tween.js@18.6.4@tween.umd.min.js