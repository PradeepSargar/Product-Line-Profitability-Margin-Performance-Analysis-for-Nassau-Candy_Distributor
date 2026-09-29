"""
Integration test suite for Nassau Candy Streamlit Dashboard and Analytical Engine.
Validates reconciliation controls, filtering behaviors, and chart builders.
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
from src.visualization import charts


class TestNassauCandyDashboardIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load and prepare full dataset once for integration tests."""
        cls.df = get_clean_dataset()
        cls.prod_df = profitability.compute_product_profitability(cls.df)

    def test_section_27_reconciliation_controls(self):
        """Verify all control values from Section 27 reconcile to the cent/percent."""
        kpis = profitability.compute_overall_kpis(self.df)

        # 1. Total Sales: 141,783.63
        self.assertAlmostEqual(kpis['total_sales'], 141783.63, places=2)

        # 2. Total Gross Profit: 93,442.80
        self.assertAlmostEqual(kpis['total_gross_profit'], 93442.80, places=2)

        # 3. Total Cost: 48,340.83
        self.assertAlmostEqual(kpis['total_cost'], 48340.83, places=2)

        # 4. Gross Margin %: 65.91%
        self.assertAlmostEqual(kpis['gross_margin_pct'], 65.91, places=2)

        # 5. Products: 15
        self.assertEqual(kpis['total_products'], 15)

        # 6. Divisions: 3
        self.assertEqual(kpis['total_divisions'], 3)

        # 7. Regions: 4
        self.assertEqual(kpis['total_regions'], 4)

        # 8. Top 5 Contribution: Profit 95.06%, Revenue 92.88%
        top5 = product_analysis.compute_top_n_contribution(self.prod_df, n=5)
        self.assertAlmostEqual(top5['top_n_profit_pct'], 95.06, places=2)
        self.assertAlmostEqual(top5['top_n_revenue_pct'], 92.88, places=2)

        # 9. Risk Flagged Products: 7
        risk_df = risk_analysis.compute_risk_screening(self.prod_df)
        risk_summary = risk_analysis.get_risk_summary(risk_df)
        self.assertEqual(risk_summary['flagged_count'], 7)

        # 10. Regional Margin Range: ~0.96 pp
        reg_df = regional_analysis.compute_regional_summary(self.df)
        reg_range = regional_analysis.compute_regional_margin_range(reg_df)
        self.assertAlmostEqual(reg_range['margin_range_pp'], 0.96, places=2)

    def test_division_controls(self):
        """Verify validated division-level figures."""
        div_df = division_analysis.compute_division_summary(self.df).set_index('Division')

        # Chocolate: 92.88% revenue, 95.06% profit, 67.45% margin
        self.assertAlmostEqual(div_df.loc['Chocolate', 'Revenue Contribution %'], 92.88, places=1)
        self.assertAlmostEqual(div_df.loc['Chocolate', 'Profit Contribution %'], 95.06, places=1)
        self.assertAlmostEqual(div_df.loc['Chocolate', 'Gross Margin %'], 67.45, places=1)

        # Other: 6.82% revenue, 4.64% profit, 44.84% margin
        self.assertAlmostEqual(div_df.loc['Other', 'Revenue Contribution %'], 6.82, places=1)
        self.assertAlmostEqual(div_df.loc['Other', 'Profit Contribution %'], 4.64, places=1)
        self.assertAlmostEqual(div_df.loc['Other', 'Gross Margin %'], 44.84, places=1)

        # Sugar: 0.30% revenue, 0.30% profit, 66.61% margin
        self.assertAlmostEqual(div_df.loc['Sugar', 'Revenue Contribution %'], 0.30, places=1)
        self.assertAlmostEqual(div_df.loc['Sugar', 'Profit Contribution %'], 0.30, places=1)
        self.assertAlmostEqual(div_df.loc['Sugar', 'Gross Margin %'], 66.61, places=1)

    def test_segmentation_quadrants(self):
        """Verify 4-quadrant product segmentation breakdown."""
        seg_df = segmentation.segment_products(self.prod_df)
        seg_counts = seg_df['Segment'].value_counts()

        # Validated: Core Driver (6), Volume Driver (2), Niche Gem (2), Underperformer (5)
        self.assertEqual(seg_counts.get('Core Driver', 0), 6)
        self.assertEqual(seg_counts.get('Volume Driver', 0), 2)
        self.assertEqual(seg_counts.get('Niche Gem', 0), 2)
        self.assertEqual(seg_counts.get('Underperformer', 0), 5)

    def test_pareto_concentration(self):
        """Verify Pareto concentration metrics."""
        rev_pareto = pareto.compute_revenue_pareto(self.prod_df)
        prof_pareto = pareto.compute_profit_pareto(self.prod_df)

        rev_count = pareto.get_pareto_threshold_count(rev_pareto, 'Cumulative Revenue %', 80)
        prof_count = pareto.get_pareto_threshold_count(prof_pareto, 'Cumulative Profit %', 80)

        # Validated: 5 products to reach 80% threshold for both
        self.assertEqual(rev_count, 5)
        self.assertEqual(prof_count, 5)

    def test_charts_build_successfully(self):
        """Verify all Plotly chart builders execute and return valid figures."""
        prod_df = self.prod_df
        div_df = division_analysis.compute_division_summary(self.df)
        reg_df = regional_analysis.compute_regional_summary(self.df)
        monthly_df = profitability.compute_time_analysis_monthly(self.df)
        yearly_df = profitability.compute_time_analysis_yearly(self.df)
        rev_pareto = pareto.compute_revenue_pareto(prod_df)
        prof_pareto = pareto.compute_profit_pareto(prod_df)
        seg_df = segmentation.segment_products(prod_df)

        figures = [
            charts.chart_revenue_vs_profit_by_product(prod_df),
            charts.chart_profit_contribution_by_product(prod_df),
            charts.chart_division_revenue_contribution(div_df),
            charts.chart_division_profit_contribution(div_df),
            charts.chart_gross_profit_by_product(prod_df),
            charts.chart_gross_margin_by_product(prod_df),
            charts.chart_revenue_vs_profit_contribution(prod_df),
            charts.chart_division_revenue_vs_profit(div_df),
            charts.chart_division_margin_comparison(div_df),
            charts.chart_division_contribution_comparison(div_df),
            charts.chart_regional_gross_profit(reg_df),
            charts.chart_regional_gross_margin(reg_df),
            charts.chart_regional_revenue_vs_profit(reg_df),
            charts.chart_cost_vs_sales_scatter(prod_df),
            charts.chart_revenue_pareto(rev_pareto),
            charts.chart_profit_pareto(prof_pareto),
            charts.chart_monthly_sales_profit(monthly_df),
            charts.chart_monthly_margin(monthly_df),
            charts.chart_yearly_comparison(yearly_df),
            charts.chart_yearly_margin(yearly_df),
            charts.chart_strategic_matrix(seg_df),
            charts.chart_revenue_profit_contribution_scatter(prod_df),
            charts.chart_margin_distribution(self.df, group_col='Division'),
            charts.chart_margin_distribution(self.df, group_col='Region'),
        ]

        for i, fig in enumerate(figures):
            self.assertIsNotNone(fig, f"Figure {i} is None")
            self.assertTrue(hasattr(fig, 'to_dict'), f"Figure {i} lacks to_dict method")


if __name__ == '__main__':
    unittest.main()
