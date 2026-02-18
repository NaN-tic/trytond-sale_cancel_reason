
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from datetime import timedelta

from trytond.i18n import gettext
from trytond.modules.account.tests import create_chart
from trytond.modules.company.tests import (
    CompanyTestMixin, create_company, set_company)
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction


class SaleCancelReasonTestCase(CompanyTestMixin, ModuleTestCase):
    'Test SaleCancelReason module'
    module = 'sale_cancel_reason'

    @with_transaction()
    def test_cancel_description_on_cancel(self):
        'Test cancel description on cancel and expired quotation'
        pool = Pool()
        Party = pool.get('party.party')
        Sale = pool.get('sale.sale')
        PaymentTerm = pool.get('account.invoice.payment_term')
        CancelReason = pool.get('sale.cancel.reason')
        Date = pool.get('ir.date')

        company = create_company()
        with set_company(company):
            create_chart(company)

            party, = Party.create([{
                        'name': 'Party',
                        'addresses': [
                            ('create', [{}]),
                            ],
                        }])
            payment_term, = PaymentTerm.create([{
                        'name': 'Test',
                        'lines': [
                            ('create', [{
                                        'type': 'remainder',
                                        }])
                            ],
                        }])
            cancel_reason, = CancelReason.create([{
                        'name': 'Cancel Reason',
                        }])

            sale_manual, = Sale.create([{
                        'party': party.id,
                        'company': company.id,
                        'payment_term': payment_term.id,
                        'currency': company.currency.id,
                        'invoice_address': party.addresses[0].id,
                        'shipment_address': party.addresses[0].id,
                        'lines': [
                            ('create', [{
                                        'description': 'Test',
                                        'quantity': 1,
                                        'unit_price': 1,
                                        }]),
                            ],
                        }])
            Sale.quote([sale_manual])
            sale_manual.cancel_reason = cancel_reason
            sale_manual.cancel_description = 'Manual cancel'
            sale_manual.save()
            Sale.cancel([sale_manual])
            self.assertEqual(sale_manual.state, 'cancelled')
            self.assertEqual(sale_manual.cancel_description, 'Manual cancel')
            Sale.draft([sale_manual])
            sale_manual = Sale(sale_manual.id)
            self.assertEqual(sale_manual.state, 'draft')
            self.assertIsNone(sale_manual.cancel_description)

            sale_expired, = Sale.create([{
                        'party': party.id,
                        'company': company.id,
                        'payment_term': payment_term.id,
                        'currency': company.currency.id,
                        'invoice_address': party.addresses[0].id,
                        'shipment_address': party.addresses[0].id,
                        'lines': [
                            ('create', [{
                                        'description': 'Test',
                                        'quantity': 1,
                                        'unit_price': 1,
                                        }]),
                            ],
                        }])
            Sale.quote([sale_expired])
            sale_expired.sale_date = Date.today() - timedelta(days=5)
            sale_expired.quotation_date = Date.today() - timedelta(days=5)
            sale_expired.quotation_validity = timedelta(days=1)
            sale_expired.save()
            Sale.cancel_expired_quotation()
            sale_expired = Sale(sale_expired.id)
            self.assertEqual(sale_expired.state, 'cancelled')
            self.assertEqual(
                sale_expired.cancel_description,
                gettext(
                    'sale_cancel_reason.msg_sale_cancelled_expired_quotation'))


del ModuleTestCase
