"""
Unit and integration tests for dashboard pages, components, and numerical reconciliation.
"""

import unittest
import pandas as pd
import numpy as np

from src.data.cleaning import get_clean_dataset
from src.analysis import (
    profitability,
    product_analysis,
    pareto,
    division_analysis,
    regional_analysis,
    segmentation,
    risk_analysis,
)
from dashboard.pages import (
    executive_overview,
    product_profitability,
    business_performance,
    strategic_analysis,
    risk_diagnostics,
)
from dashboard.components import kpi_cards, tables, insights, header
from dashboard.utils import dashboard_utils


class TestDashboardPagesAndReconciliation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = get_clean_dataset()

    def test_reconciliation_exact_benchmarks(self):
        """Reconcile against Section 34 & Section 19 validated notebook controls."""
        kpis = profitability.compute_overall_kpis(self.df)
        prod_df = profitability.compute_product_profitability(self.df)
        top5 = product_analysis.compute_top_n_contribution(prod_df, 5)
        risk_df = risk_analysis.compute_risk_screening(prod_df)
        risk_summary = risk_analysis.get_risk_summary(risk_df)
        reg_df = regional_analysis.compute_regional_summary(self.df)
        reg_range = regional_analysis.compute_regional_margin_range(reg_df)

        self.assertAlmostEqual(kpis['total_sales'], 141783.63, places=2)
        self.assertAlmostEqual(kpis['total_cost'], 48340.83, places=2)
        self.assertAlmostEqual(kpis['total_gross_profit'], 93442.80, places=2)
        self.assertAlmostEqual(kpis['gross_margin_pct'], 65.91, places=2)
        self.assertEqual(kpis['total_units'], 38654)
        self.assertEqual(kpis['total_products'], 15)
        self.assertEqual(kpis['total_divisions'], 3)
        self.assertEqual(kpis['total_regions'], 4)
        self.assertAlmostEqual(top5['top_n_revenue_pct'], 92.88, places=2)
        self.assertAlmostEqual(top5['top_n_profit_pct'], 95.06, places=2)
        self.assertEqual(risk_summary['flagged_count'], 7)
        self.assertAlmostEqual(reg_range['margin_range_pp'], 0.96, places=2)

    def test_page_renders_with_full_data(self):
        """Ensure all 5 pages execute their render methods without uncaught exceptions."""
        filter_config = {
            'min_margin': 0.0,
            'is_active': False,
        }
        pages = [
            executive_overview,
            product_profitability,
            business_performance,
            strategic_analysis,
            risk_diagnostics,
        ]
        for page in pages:
            # Should run without error
            page.render(self.df, self.df, filter_config)

    def test_page_renders_with_empty_data(self):
        """Ensure all 5 pages execute empty-state logic gracefully without crashing."""
        empty_df = self.df.iloc[0:0]
        filter_config = {
            'min_margin': 0.0,
            'is_active': True,
        }
        pages = [
            executive_overview,
            product_profitability,
            business_performance,
            strategic_analysis,
            risk_diagnostics,
        ]
        for page in pages:
            page.render(empty_df, self.df, filter_config)


if __name__ == '__main__':
    unittest.main()
