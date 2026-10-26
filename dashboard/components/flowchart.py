"""
Execution Workflow Flowchart component for Nassau Candy Analytics.
Renders a professional, executive-grade end-to-end analytical pipeline flowchart
based on the Nassau Candy Project Execution Workflow.
"""

from dashboard.utils.dashboard_utils import render_html


def render_workflow_flowchart(expanded: bool = True):
    """
    Render a clean, professional end-to-end workflow flowchart
    mapping the complete data engineering, diagnostic, and decision-support pipeline.
    """
    flowchart_html = """
        <div class="flowchart-container">
            <div class="flowchart-header">
                <div class="flowchart-title">
                    <span style="font-size: 1.3rem;">⚡</span>
                    <span>End-to-End Analytical Pipeline &amp; Execution Workflow</span>
                </div>
                <div>
                    <span class="flowchart-badge">✓ Validated Methodology</span>
                </div>
            </div>
            <div class="flowchart-steps">
                <!-- Step 1 -->
                <div class="flowchart-step-card">
                    <div>
                        <div class="flowchart-step-num">Step 01</div>
                        <div class="flowchart-step-title">🧹 Data Cleaning &amp; Validation</div>
                        <div class="flowchart-step-desc">
                            9,994 order rows sanitized. Order vs Ship date isolation, null resolution &amp; strict schema verification.
                        </div>
                    </div>
                    <div class="flowchart-step-status">✓ 100% Integrity</div>
                </div>
                
                <!-- Step 2 -->
                <div class="flowchart-step-card">
                    <div>
                        <div class="flowchart-step-num">Step 02</div>
                        <div class="flowchart-step-title">⚙️ Metric Engine &amp; Margins</div>
                        <div class="flowchart-step-desc">
                            COGS &amp; Gross Profit calculation. Gross Margin %, unit economics, and multi-tier contribution formulas.
                        </div>
                    </div>
                    <div class="flowchart-step-status">✓ $93.4K GP Benchmarked</div>
                </div>
                
                <!-- Step 3 -->
                <div class="flowchart-step-card">
                    <div>
                        <div class="flowchart-step-num">Step 03</div>
                        <div class="flowchart-step-title">📊 Multi-Tier Diagnostics</div>
                        <div class="flowchart-step-desc">
                            Division asymmetry modeling, regional margin spread analysis (0.96 pp), and cost-vs-sales diagnostics.
                        </div>
                    </div>
                    <div class="flowchart-step-status">✓ 3 Divisions · 4 Territories</div>
                </div>
                
                <!-- Step 4 -->
                <div class="flowchart-step-card">
                    <div>
                        <div class="flowchart-step-num">Step 04</div>
                        <div class="flowchart-step-title">🎯 Strategic Segmentation</div>
                        <div class="flowchart-step-desc">
                            80/20 Pareto concentration curves and 4-quadrant matrix (Core Drivers, Volume, Niche Gems, Underperformers).
                        </div>
                    </div>
                    <div class="flowchart-step-status">✓ 4 Quadrants Classified</div>
                </div>
                
                <!-- Step 5 -->
                <div class="flowchart-step-card">
                    <div>
                        <div class="flowchart-step-num">Step 05</div>
                        <div class="flowchart-step-title">🚀 Executive BI Platform</div>
                        <div class="flowchart-step-desc">
                            Interactive Streamlit dashboard with dynamic cross-filters, real-time date windowing, and KPI drill-downs.
                        </div>
                    </div>
                    <div class="flowchart-step-status">✓ Production Ready</div>
                </div>
            </div>
        </div>
    """
    render_html(flowchart_html)
