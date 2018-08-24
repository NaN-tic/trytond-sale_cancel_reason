# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['CancelReason', 'Sale', 'Opportunity']



class CancelReason(ModelSQL, ModelView):
    'Sale Cancel Reason'
    __name__ = 'sale.cancel.reason'
    name = fields.Char('Name', translate=True)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    cancel_reason = fields.Many2One('sale.cancel.reason', 'Cancel Reason',
        states={
            'required': ((Eval('state') == 'cancel')
                & ~Eval('context', {}).get('sale_force_cancel', False)),
            'readonly': Eval('state') == 'cancel',
            },
        depends=['state'])
    cancel_description = fields.Text('Cancel Description',
        states={
            'required': ((Eval('state') == 'cancel')
                & ~Eval('context', {}).get('sale_force_cancel', False)),
            'readonly': Eval('state') == 'cancel',
            },
        depends=['state'])

    @classmethod
    def delete(cls, sales):
        with Transaction().set_context(sale_force_cancel=True):
            super(Sale, cls).delete(sales)


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'

    lost_reason_type = fields.Many2One('sale.cancel.reason', 'Lost Reason',
        states={
            'required': Eval('state') == 'lost',
            'readonly': Eval('state') == 'lost',
            },
        depends=['state'])

    @classmethod
    def __setup__(cls):
        super(Opportunity, cls).__setup__()
        cls.lost_reason.states = {
            'required': Eval('state') == 'lost',
            'readonly': Eval('state') == 'lost',
            }
