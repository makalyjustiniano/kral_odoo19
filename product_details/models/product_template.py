# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re



class ProductTemplate(models.Model):
    _inherit = 'product.template'


    flex_code = fields.Char(string="Código FLEX", help="Código FLEX del producto.")
    group = fields.Char(string="Grupo", help="Grupo del producto.")
    brand = fields.Char(string="Marca", help="Marca del producto.")

    net_weight = fields.Float(string="Peso Neto", help="Peso neto del producto.", digits=(16, 4))
    gross_weight = fields.Float(string="Peso Bruto", help="Peso bruto del producto.", digits=(16, 4))

    net_volume = fields.Float(string="Volumen Neto", help="Volumen neto del producto.", digits=(16, 4))
    gross_volume = fields.Float(string="Volumen Bruto", help="Volumen bruto del producto.", digits=(16, 4))


    unidad_medida_siat = fields.Float(string="Unidad de Medida SIAT", help="Unidad de medida según SIAT.")
    description_unidad_medida_siat = fields.Char(string="Descripción Unidad de Medida SIAT", help="Descripción de la unidad de medida según SIAT.")
    
    product_line_product = fields.Many2one('product.details', string="Producto", help="Producto.")
    product_line_group = fields.Many2one('group.details', string="Grupo", help="Grupo.")

    procedencia = fields.Char(string="Procedencia", help="Procedencia del producto.")
    vida_util = fields.Float(string="Vida Útil", help="Vida útil del producto.")
    detalles_mataterias_primas = fields.Text(string="Detalles de Materias Primas", help="Detalles de las materias primas del producto.")
    capacidad_almacenamiento = fields.Text(string="Capacidad de Almacenamiento", help="Capacidad de almacenamiento del producto.")
    modo_conservacion = fields.Text(string="Modo de Conservación", help="Modo de conservación del producto.")
    ### Fields of technical data sheets
    #prop_organolepticas = fields.Html(string="Propiedades Organolépticas", help="Propiedades Organolépticas del producto.")
    #prop_fisico_quimicas = fields.Html(string="Propiedades Físico-Químicas", help="Propiedades Físico-Químicas del producto.")
    #data_microbologicos = fields.Html(string="Datos Microbiológicos", help="Datos Microbiológicos del producto.")
    #info_nutricional = fields.Html(string="Información Nutricional", help="Información Nutricional del producto.")

    limit_discount_percentage = fields.Float(string="Porcentaje Límite de Descuento %", help="Porcentaje límite de descuento para el producto.")


    ## Consumption Table
    form_consumption = fields.Text(string="Forma de Consumo", help="Forma de consumo del producto.")
    intented_use = fields.Text(strin='Uso Previsto', help="Uso previsto del producto.")
    intented_no_use = fields.Text(string="Uso No Previsto", help="Uso no previsto del producto.")
    destination = fields.Text(string="Destinación", help="Destinación del producto.")


    ## Ingredientes and additives table
    ingredients = fields.Text(string="Ingredientes", help="Ingredientes del producto.")
    additives_ids = fields.One2many('line.additives', 'product_template_id', string="Aditivos", help="Aditivos del producto.")

    ## Organoleptic properties table
    aspect = fields.Char(string="Aspecto", help="Aspecto del producto.")
    color_custom = fields.Char(string="Color", help="Color del producto.")
    scent = fields.Char(string="Aroma", help="Aroma del producto.")
    flavor = fields.Char(string="Sabor", help="Sabor del producto.")


    ## Physical-chemical properties table
    physical_chemical_ids = fields.One2many('physical.chemical.property', 'product_template_id', string="Propiedades Físico-Químicas", help="Propiedades físico-químicas del producto.")
    
    ## Microbiological data table
    microbiological_ids = fields.One2many('microbiological.data', 'product_template_id', string="Datos Microbiológicos", help="Datos microbiológicos del producto.")    


    ## Nutritional information table
    nutritional_info = fields.One2many( 'information.nutricional', 'product_template_id', string="Información Nutricional Detallada",  help="Información nutricional detallada del producto.")
    nutricional_notes = fields.Text(string="Notas de Información Nutricional", help="Notas adicionales sobre la información nutricional del producto.")


    ## Alergenos Information
    alergenos_ids = fields.One2many('product.allergens.line', 'product_template_id' ,string="Alergenos", help="Alergenos del producto.")
    
    @api.onchange('categ_id')
    def _onchange_category_code(self):
        for product in self:
            code = ""
            if product.categ_id and product.categ_id.category_code:
                prefix = product.categ_id.category_code
                products = self.env['product.template'].search([
                    ('categ_id', '=', product.categ_id.id),
                    ('default_code', '!=', False),
                ])

                pattern = re.compile(r"(\d+)$")
                max_num = 0
                max_len = 0
                for p in products:
                    dc = (p.default_code or '').strip()
                    m = pattern.search(dc)
                    if m:
                        num_str = m.group(1)
                        try:
                            num = int(num_str)
                        except ValueError:
                            continue
                        if num > max_num:
                            max_num = num
                        if len(num_str) > max_len:
                            max_len = len(num_str)

                width = max_len if max_len > 0 else 3
                next_num = max_num + 1
                next_num_str = str(next_num).zfill(width)
                code = f"{prefix}-{next_num_str}"

            product.default_code = code





    

