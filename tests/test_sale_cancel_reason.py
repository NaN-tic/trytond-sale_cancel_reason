#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends  # , doctest_dropdb TODO: Remove if no sceneario needed.


class TestCase(unittest.TestCase):
    'Test module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('sale_cancel_reason')

    def test0005views(self):
        'Test views'
        test_view('sale_cancel_reason')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    # TODO: remove if no scenario needed.
    #suite.addTests(doctest.DocFileSuite('scenario_sale_cancel_reason.rst',
    #        setUp=doctest_dropdb, tearDown=doctest_dropdb, encoding='utf-8',
    #        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
