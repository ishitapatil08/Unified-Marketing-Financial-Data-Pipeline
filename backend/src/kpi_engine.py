import duckdb
import pandas as pd

class KPIEngine:
    def __init__(self, db_path='data/warehouse.duckdb'):
        self.db_path = db_path

    def _execute_query(self, query):
        with duckdb.connect(self.db_path) as conn:
            return conn.execute(query).df()

    def get_executive_summary(self):
        query = """
        WITH finance AS (
            SELECT 
                SUM(revenue) as total_revenue,
                SUM(gross_profit) as total_gross_profit,
                SUM(net_profit) as total_net_profit
            FROM fact_financials
        ),
        marketing AS (
            SELECT 
                SUM(spend) as total_ad_spend,
                SUM(conversions) as total_conversions
            FROM fact_marketing
        )
        SELECT 
            f.total_revenue,
            f.total_gross_profit,
            f.total_net_profit,
            m.total_ad_spend,
            m.total_conversions,
            (f.total_revenue / NULLIF(m.total_ad_spend, 0)) as profit_adjusted_roas,
            (m.total_ad_spend / NULLIF(m.total_conversions, 0)) as cost_per_acquisition
        FROM finance f, marketing m
        """
        return self._execute_query(query).to_dict(orient='records')[0]

    def get_financial_kpis_by_month(self):
        query = """
        SELECT 
            EXTRACT(YEAR FROM date_key) as year,
            EXTRACT(MONTH FROM date_key) as month,
            SUM(revenue) as revenue,
            SUM(net_profit) as net_profit
        FROM fact_financials
        GROUP BY 1, 2
        ORDER BY 1, 2
        """
        return self._execute_query(query).to_dict(orient='records')
        
    def get_marketing_kpis_by_campaign(self):
        query = """
        SELECT 
            campaign_id,
            SUM(spend) as spend,
            SUM(impressions) as impressions,
            SUM(clicks) as clicks,
            SUM(conversions) as conversions,
            CASE WHEN SUM(clicks) > 0 THEN SUM(conversions)*1.0/SUM(clicks) ELSE 0 END as conv_rate,
            CASE WHEN SUM(conversions) > 0 THEN SUM(spend)/SUM(conversions) ELSE 0 END as cost_per_acquisition
        FROM fact_marketing
        GROUP BY 1
        ORDER BY spend DESC
        """
        return self._execute_query(query).to_dict(orient='records')

if __name__ == "__main__":
    engine = KPIEngine()
    print(engine.get_executive_summary())
