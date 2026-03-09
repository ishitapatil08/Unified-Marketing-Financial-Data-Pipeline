import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_financial_data(rows=1000):
    np.random.seed(42)
    dates = [datetime(2023, 1, 1) + timedelta(days=int(i)) for i in np.random.randint(0, 365, rows)]
    categories = ['Electronics', 'Software', 'Consulting', 'Hardware']
    products = ['Product A', 'Product B', 'Product C']
    
    data = {
        'transaction_id': [f"TXN-{i:05d}" for i in range(rows)],
        'date': dates,
        'category': np.random.choice(categories, rows),
        'product': np.random.choice(products, rows),
        'revenue': np.random.uniform(50, 5000, rows).round(2),
        'cogs': np.random.uniform(10, 2000, rows).round(2), # Cost of Goods Sold
        'region': np.random.choice(['North America', 'EMEA', 'APAC'], rows)
    }
    df = pd.DataFrame(data)
    # Add some dirty data to simulate missing/inconsistent values for ETL step
    df.loc[::50, 'revenue'] = np.nan
    df.loc[::100, 'region'] = np.nan
    return df

def generate_marketing_data(rows=500):
    np.random.seed(101)
    dates = [datetime(2023, 1, 1) + timedelta(days=int(i)) for i in np.random.randint(0, 365, rows)]
    platforms = ['Google Ads', 'Facebook', 'LinkedIn', 'Email']
    campaigns = ['Q1_Launch', 'Summer_Promo', 'Black_Friday', 'Retargeting']
    
    data = {
        'campaign_id': [f"CMP-{i:04d}" for i in range(rows)],
        'date': dates,
        'platform': np.random.choice(platforms, rows),
        'campaign_name': np.random.choice(campaigns, rows),
        'impressions': np.random.randint(1000, 100000, rows),
        'clicks': np.random.randint(50, 5000, rows),
        'spend': np.random.uniform(10, 1000, rows).round(2),
        'conversions': np.random.randint(0, 500, rows)
    }
    df = pd.DataFrame(data)
    # Dirty data
    df.loc[::75, 'clicks'] = 0 # To simulate zero clicks (prevent div by zero in ETL)
    return df

def main():
    os.makedirs('data/raw', exist_ok=True)
    
    df_finance = generate_financial_data(2000)
    df_finance.to_csv('data/raw/financial_transactions.csv', index=False)
    
    df_marketing = generate_marketing_data(800)
    df_marketing.to_csv('data/raw/marketing_performance.csv', index=False)
    
    print("Mock data generated in data/raw/")

if __name__ == "__main__":
    main()
