__menu = {
    'uri': __package__,
    'name': '숫자 야구',
    'list': [
        {
            'uri': 'main',
            'name': 'Main',
        },
        {
            'uri': 'log',
            'name': '로그',
        },
    ]
}


setting = {
    'filepath' : __file__,
    'use_db': False,
    'use_default_setting': False,
    'home_module': None,
    'menu': __menu,
    'setting_menu': None,
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)

from .mod_main import ModuleMain

P.set_module_list([ModuleMain])

