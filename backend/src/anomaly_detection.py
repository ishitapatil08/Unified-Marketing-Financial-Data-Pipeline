import duckdb
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import os

class AnomalyDetector:
    def __init__(self, db_path='data/warehouse.duckdb'):
        self.db_path = db_path
        
    def _execute_query(self, query):
        with duckdb.connect(self.db_path) as conn:
            return conn.execute(query).df()
            
    def detect_financial_anomalies(self):
        print("Running Isolation Forest on Financial Revenue...")
        df = self._execute_query("SELECT transaction_id, date_key, revenue, cogs, gross_profit FROM fact_financials")
        if df.empty:
            return []
            
        # We'll use revenue and cogs for anomaly detection
        features = df[['revenue', 'cogs']].fillna(0)
        
        # Isolation Forest
        clf = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
        df['anomaly'] = clf.fit_predict(features)
        
        # Output anomalies (-1)
        anomalies = df[df['anomaly'] == -1]
        print(f"Detected {len(anomalies)} financial anomalies.")
        return anomalies.to_dict(orient='records')

    def detect_marketing_anomalies(self):
        print("Running Isolation Forest on Marketing Spend & Conv Rate...")
        df = self._execute_query("SELECT campaign_id, date_key, spend, clicks, conversion_rate FROM fact_marketing")
        if df.empty:
            return []
            
        features = df[['spend', 'clicks', 'conversion_rate']].fillna(0)
        
        clf = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
        df['anomaly'] = clf.fit_predict(features)
        
        anomalies = df[df['anomaly'] == -1]
        print(f"Detected {len(anomalies)} marketing anomalies.")
        return anomalies.to_dict(orient='records')
        
if __name__ == "__main__":
    detector = AnomalyDetector()
    fin_anomalies = detector.detect_financial_anomalies()
    mkt_anomalies = detector.detect_marketing_anomalies()
