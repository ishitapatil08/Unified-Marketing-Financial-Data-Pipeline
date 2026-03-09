import duckdb
import os

def connect_or_create_dw(db_path='data/warehouse.duckdb'):
    conn = duckdb.connect(db_path)
    return conn

def setup_star_schema(conn):
    print("Setting up Star Schema...")
    
    # Dimension Tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key DATE PRIMARY KEY,
            year INT,
            month INT,
            quarter INT,
            day_of_week INT
        );
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id VARCHAR PRIMARY KEY,
            product_category VARCHAR
        );
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_campaign (
            campaign_id VARCHAR PRIMARY KEY,
            campaign_name VARCHAR,
            platform VARCHAR
        );
    """)
    
    # Fact Tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fact_financials (
            transaction_id VARCHAR PRIMARY KEY,
            date_key DATE,
            product_id VARCHAR,
            region VARCHAR,
            revenue DECIMAL(10,2),
            cogs DECIMAL(10,2),
            gross_profit DECIMAL(10,2),
            net_profit DECIMAL(10,2)
        );
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fact_marketing (
            campaign_id VARCHAR,
            date_key DATE,
            impressions INT,
            clicks INT,
            spend DECIMAL(10,2),
            conversions INT,
            ctr DECIMAL(10,4),
            cpc DECIMAL(10,4),
            conversion_rate DECIMAL(10,4)
        );
    """)

def load_data(conn):
    print("Loading data into Data Warehouse...")
    finance_path = 'data/processed/financial_transactions_clean.csv'
    marketing_path = 'data/processed/marketing_performance_clean.csv'
    
    if not os.path.exists(finance_path) or not os.path.exists(marketing_path):
        print("Processed data not found. Run ETL first.")
        return
        
    # Load Fact Financials
    conn.execute(f"""
        INSERT INTO fact_financials
        SELECT 
            transaction_id, CAST(date AS DATE), product, region, 
            revenue, cogs, gross_profit, net_profit
        FROM read_csv_auto('{finance_path}', ignore_errors=true)
        ON CONFLICT DO NOTHING;
    """)
    
    # Load Fact Marketing
    conn.execute(f"""
        INSERT INTO fact_marketing
        SELECT 
            campaign_id, CAST(date AS DATE), impressions, clicks, 
            spend, conversions, ctr, cpc, conversion_rate
        FROM read_csv_auto('{marketing_path}', ignore_errors=true);
    """)
    
    # Re-populate Dim Date based on facts
    conn.execute("""
        INSERT INTO dim_date
        SELECT DISTINCT 
            date_key,
            EXTRACT(year FROM date_key),
            EXTRACT(month FROM date_key),
            EXTRACT(quarter FROM date_key),
            EXTRACT(dayofweek FROM date_key)
        FROM (
            SELECT date_key FROM fact_financials
            UNION
            SELECT date_key FROM fact_marketing
        )
        ON CONFLICT DO NOTHING;
    """)
    
    print("Data loaded perfectly.")

def main():
    os.makedirs('data', exist_ok=True)
    conn = connect_or_create_dw()
    setup_star_schema(conn)
    load_data(conn)
    conn.close()

if __name__ == "__main__":
    main()
