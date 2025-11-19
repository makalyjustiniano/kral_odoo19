# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import re


class ProductLine(models.Model):
    _name = 'product.details'

    name = fields.Char(string="Producto", help="Producto.")
    description = fields.Text(string="Descripción Detalle", help="Descripción del Producto.")


class ProductGroup(models.Model):
    _name = 'group.details'

    name = fields.Char(string="Grupo", help="Grupo del producto.")
    description = fields.Text(string="Descripción Detalle", help="Descripción del grupo del producto.")


class LineAdditivesName(models.Model):
    _name = 'additives.name'

    name = fields.Char(string="Nombre Aditivo", help="Nombre del aditivo del producto.")
    description = fields.Text(string="Descripción Nombre Aditivo", help="Descripción del nombre del aditivo del producto.")

class LineAdditives(models.Model):
    _name = 'line.additives'

    additive_name_id = fields.Many2one('additives.name', string="Nombre", help="Nombre del aditivo del producto.")
    name = fields.Text(string="Descripción Aditivo", help="Descripción del aditivo del producto.")
    code = fields.Char(string="Código", help="Código del aditivo del producto.")
    weight = fields.Float(string="Peso g/kg", help="Peso del aditivo del producto.", digits=(16, 4))
    product_template_id = fields.Many2one('product.template', string="Producto", help="Producto asociado al aditivo.")


class PyhsicalChemicalName(models.Model):
    _name = 'physical.chemical.name'
    name = fields.Char(string="Nombre Propiedad Físico-Química", help="Nombre de la propiedad físico-química del producto.")
    description = fields.Text(string="Descripción Propiedad Físico-Química", help="Descripción de la propiedad físico-química del producto.")

class PhysicalChemicalProperty(models.Model):
    _name = 'physical.chemical.property'

    physical_chemical_name_id = fields.Many2one('physical.chemical.name', string="Parámetro", help="Nombre de la propiedad físico-química asociada.")
    name = fields.Char(string="Propiedad Físico-Química", help="Propiedad físico-química del producto.")
    method = fields.Char(string="Método", help="Método de la propiedad físico-química.")
    min = fields.Float(string="Min", help="Valor mínimo de la propiedad físico-química.", digits=(16, 4))
    max = fields.Float(string="Max", help="Valor máximo de la propiedad físico-química.", digits=(16, 4))
    unit = fields.Char(string="Unid", help="Unidad de la propiedad físico-química.")
    product_template_id = fields.Many2one('product.template', string="Producto", help="Producto asociado a la propiedad físico-química.")

class MicrobiologicalName(models.Model):
    _name = 'microbiological.name'

    name = fields.Char(string="Recuentos", help="Recuentos microbiológico.")
    description = fields.Text(string="Descripción Recuentos", help="Descripción de los recuentos microbiológicos.")


class MicrobiologicalData(models.Model):
    _name = 'microbiological.data'

    microbiological_name_id = fields.Many2one('microbiological.name', string="Recuentos", help="Recuento microbiológico asociado.")
    name = fields.Text(string="Recuentos", help="Descripción del recuento microbiológico.")
    limit_permitted_n = fields.Float(string="N", help="Límite permitido N del recuento microbiológico.")
    limit_permitted_c = fields.Float(string="c", help="Límite permitido c del recuento microbiológico.")
    limit_permitted_m_ufc_g = fields.Float(string="m (UFC/g)", help="Límite permitido M en UFC/g del recuento microbiológico.")
    limit_permitted_m = fields.Float(string="M", help="Límite permitido M del recuento microbiológico.")

    product_template_id = fields.Many2one('product.template', string="Producto", help="Producto asociado al recuento microbiológico.")

class InformationNutricionalName(models.Model):
    _name = 'information.nutricional.name'

    name = fields.Char(string="Nombre Información Nutricional", help="Nombre de la información nutricional del producto.")
    description = fields.Text(string="Descripción Información Nutricional", help="Descripción de la información nutricional del producto.")



class InformationNutricional(models.Model):
    _name = 'information.nutricional'

    nutricional_name_id = fields.Many2one('information.nutricional.name', string="Info Nutricional", help="Nombre de la información nutricional asociada.")
    name = fields.Char(string="Nombre Información Nutricional", help="Nombre de la información nutricional del producto.")
    information = fields.Text(string="Información Nutricional", help="Información nutricional del producto.")
    by_g = fields.Char(string="100 g", help="Cantidad por gramo.")
    by_ration = fields.Char(string="Ración", help="Cantidad por ración.")
    por_ration_percentage = fields.Char(string="%Ración", help="Porcentaje por ración.")   
    product_template_id = fields.Many2one('product.template', string="Producto", help="Producto asociado a la información nutricional.")


class ProductAllergens(models.Model):
    _name = 'product.allergens'

    name = fields.Char(string="Alergeno", help="Nombre del alérgeno.")
    description = fields.Text(string="Descripción Alergeno", help="Descripción del alérgeno del producto.")


class ProductAlergensLine(models.Model):
    _name = 'product.allergens.line'

    allergen_id = fields.Many2one('product.allergens', string="Alergeno", help="Alergeno asociado.")
    anser_value_no = fields.Boolean(string="No", help="Indica si el alérgeno no está presente.", default=True)
    anser_value_yes = fields.Boolean(string="Sí", help="Indica si el alérgeno está presente.")
    puede_contener = fields.Boolean(string="Puede Contener", help="Indica si el alérgeno puede estar presente.")
    especificar_producto = fields.Char(string="Especificar Producto", help="Especificación del producto relacionado con el alérgeno.")
    product_template_id = fields.Many2one('product.template', string="Producto", help="Producto asociado al alérgeno.")