#! /usr/bin/python

{
    'name': 'wizard_precios_proveedores',
    'version': '1.0',
    'depends': ["base","stock"],
    'author': 'Latinux Sistemas',
    'category': 'Modules',
    'description': """ wizard para modificar el precio de un producto segun proveedor y categoria de producto """,
    'init_xml': ['wizard_precio_proveedores_view.xml'],
    'update_xml': ['wizard_precio_proveedores_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'certificate': 'certificate',
} 
