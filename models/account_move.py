# -*- coding: utf-8 -*-

from odoo import fields, models
import logging

class AccountMove(models.Model):
    _inherit = 'account.move'

    descuento_general = fields.Float("Descuento general")

    def calcular_descuento_general(self):
        for factura in self:
            precio_total_descuento = factura.descuento_general
            factura.eliminar_descuentos()
            if precio_total_descuento > 0:
                precio_total_factura = factura.amount_total
                for linea in factura.invoice_line_ids:
                    descuento = (precio_total_descuento / precio_total_factura) * 100
                    factura.write({ 'invoice_line_ids': [[1, linea.id, { 'discount': descuento }]] })
        return True

    def eliminar_descuentos(self):
        for linea in self.invoice_line_ids:
            if linea.discount > 0:
                self.write({ 'invoice_line_ids': [[1, linea.id, { 'discount': 0 }]] })
        return True
