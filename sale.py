# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class CancelReason(ModelSQL, ModelView):
    'Sale Cancel Reason'
    __name__ = 'sale.cancel.reason'
    name = fields.Char('Name', translate=True)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    cancel_reason = fields.Many2One('sale.cancel.reason', 'Cancel Reason',
        states={
            'required': ((Eval('state') == 'cancelled')
                & ~Eval('context', {}).get('sale_force_cancel', False)),
            'readonly': Eval('state') == 'cancelled',
            })
    cancel_description = fields.Text('Cancel Description',
        states={
            'required': ((Eval('state') == 'cancelled')
                & ~Eval('context', {}).get('sale_force_cancel', False)),
            'readonly': Eval('state') == 'cancelled',
            })

    @classmethod
    def delete(cls, sales):
        with Transaction().set_context(sale_force_cancel=True):
            super().delete(sales)

    @classmethod
    @ModelView.button
    def cancel(cls, sales):
        Opportunity = Pool().get('sale.opportunity')
        to_save = []
        for sale in sales:
            if isinstance(sale.origin, Opportunity):
                to_save.append(sale.origin)
                if not sale.origin.lost_reason_type:
                    sale.origin.lost_reason_type = sale.cancel_reason
                if not sale.origin.lost_reason:
                    sale.origin.lost_reason = sale.cancel_description
        Opportunity.save(to_save)
        super().cancel(sales)


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'

    lost_reason_type = fields.Many2One('sale.cancel.reason', 'Lost Reason',
        states={
            'required': Eval('state') == 'lost',
            'readonly': Eval('state') == 'lost',
            })

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.lost_reason.states = {
            'required': Eval('state') == 'lost',
            'readonly': Eval('state') == 'lost',
            }
