#! /usr/bin/python

from osv import *
import tools
import netsvc
from osv.orm import orm_memory
from time import *

class wizard_precios_proveedores(osv.osv_memory):

	_name = 'precios.proveedores.wizard'
	_columns = {
			'proveedor': fields.many2one('res.partner', string='Proveedores', required=False, search=True),
			'category_id': fields.many2one('product.category', string='Categorias', required=False, search=True),
			'product_id': fields.many2one('product.product', string='Productos', required=False, search=True),			
			'average':fields.float("Porcentaje", digits=(3,2)),
			'all_products':fields.boolean("Todos los productos", help="Marque este campo si desea modificar el precio de todos los productos de todos los proveedores."),
			'standard_price':fields.boolean("Precio de venta"),
			'list_price':fields.boolean("Precio de compra"),
			'state':fields.selection([('hecho', 'Finalizado'),('choosing', 'En proceso'),('choosed-prov', 'prov elegido'),('choosed-cat','cat elegido'),('choosed-prod','prod elegido')],'Estado',invisible=True)
	}
	
	_defaults = {
			'all_products':lambda *a:False,
			'list_price':lambda *a:False,
			'standard_price':lambda *a:False,
			'state': lambda *c: 'choosing',
			'average': lambda *a: 1.0			
	}
	
	def onchange_suppliers(self,cr,uid,ids,provid):
		res = {}
		if provid:
			res['value'] = {'state':'choosed-prov'}
		else:
			res['value'] = {'state':'choosing'}		
		return res
			
	def onchange_categories(self,cr,uid,ids,catid):
		res = {}
		if catid:
			res['value'] = {'state':'choosed-cat'}
		else:
			res['value'] = {'state':'choosing'}
		return res
		
	def onchange_products(self,cr,uid,ids,prodid):
		res = {}
		if prodid:
			res['value'] = {'state':'choosed-prod'}
		else:
			res['value'] = {'state':'choosing'}
		return res
		
	def accion(self,cr,uid,ids,context={}):
		
		this = self.browse(cr, uid, ids)		
		tmpl = self.pool.get('product.template') 
		prices = []
		tmplids = []
		hp = self.pool.get('historico.precios')
		modificador = 1+this[0]['average']/100				
		if this[0]['all_products']:			
			tmplids = tmpl.search(cr,uid,[])			
		elif this[0]['category_id']:
			cid = this[0]['category_id'].id
			tmplids = tmpl.search(cr,uid,[('categ_id','=',cid)])			
		elif this[0]['proveedor']:
			provid = this[0]['proveedor'].id
			productos_proveedor = self.pool.get('product.supplierinfo')
			productos_proveedor_ids = productos_proveedor.search(cr, uid, [('name', '=', provid)])
			templates = productos_proveedor.read(cr, uid, productos_proveedor_ids, ['product_id'])			
			for t in templates:
				tmplids.append(t['product_id'][0])
		elif this[0]['product_id']:
			prodid = this[0]['product_id'].id
			template = self.pool.get('product.product').read(cr,uid,prodid,['product_tmpl_id'])		
			tmplids.append(template['product_tmpl_id'][0])			
		prices = tmpl.read(cr,uid,tmplids,['list_price','standard_price'])	
		new_prices = []		
		new_price = {}
		if this[0]['standard_price'] or this[0]['list_price']: 
			for dic in prices:
				new_price['id'] = dic['id']
				if this[0]['standard_price']:
					new_price['standard_price'] = dic['standard_price']*modificador
					new_price['list_price'] = dic['list_price']
				elif this[0]['list_price']:
					new_price['list_price'] = dic['list_price']*modificador
					new_price['standard_price'] = dic['standard_price']
				else:
					new_price['standard_price'] = dic['standard_price']
					new_price['list_price'] = dic['list_price']
				new_prices.append(new_price)
				tmpl.write(cr,uid,new_price['id'],{'standard_price':new_price['standard_price'],'list_price':new_price['list_price']},context={})
				#hp.create(cr,uid,{'tmpl_id':new_price['id'], 'standard_price':new_price['standard_price'], 'list_price':new_price['list_price'], 'fecha_y_hora': strftime("%d/%m/%Y - %H:%M:%S")})
				#hp.borrar_viejos(cr,uid,tmplids)
			
		return self.write(cr,uid,ids,{'state':'hecho'},context={})		
		
wizard_precios_proveedores()
