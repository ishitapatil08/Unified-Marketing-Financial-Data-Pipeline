import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { DollarSign, Eye, TrendingUp, Target, AlertTriangle } from 'lucide-react';

export default function ExecutiveSummary() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/kpis/executive-summary');
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loader-container"><div className="loader"></div></div>;
  if (error) return <div className="text-danger flex items-center gap-sm"><AlertTriangle /> Error: {error}</div>;

  return (
    <div className="dashboard-grid grid-cols-1">
      <div className="card-header">
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 600 }}>Company Overview</h2>
          <p className="text-secondary mt-sm">High-level financial and marketing performance metrics.</p>
        </div>
      </div>
      
      <div className="dashboard-grid grid-cols-4">
        <div className="glass-card">
          <div className="card-header">
            <span className="card-title">Total Revenue</span>
            <DollarSign className="text-success" size={20} />
          </div>
          <div className="card-value">${data.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          <div className="mt-sm text-secondary text-sm">vs Last Year (+14.2%)</div>
        </div>
        
        <div className="glass-card">
          <div className="card-header">
            <span className="card-title">Net Profit</span>
            <Target className="text-accent-primary" size={20} />
          </div>
          <div className="card-value">${data.total_net_profit.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title">Total Ad Spend</span>
            <Eye className="text-warning" size={20} />
          </div>
          <div className="card-value">${data.total_ad_spend.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
        </div>

        <div className="glass-card">
          <div className="card-header">
            <span className="card-title">Profit-Adjusted ROAS</span>
            <TrendingUp className="text-accent-secondary" size={20} />
          </div>
          <div className="card-value">{data.profit_adjusted_roas.toFixed(2)}x</div>
          <div className="mt-sm text-success text-sm">+0.4x from Q3</div>
        </div>
      </div>
    </div>
  );
}
