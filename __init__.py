# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.CancelReason,
        sale.Sale,
        sale.Opportunity,
        module='sale_cancel_reason', type_='model')
