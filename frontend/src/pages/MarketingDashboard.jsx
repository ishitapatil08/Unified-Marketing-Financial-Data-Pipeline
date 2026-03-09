import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function MarketingDashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/kpis/marketing-campaigns');
        setData(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loader-container"><div className="loader"></div></div>;

  const chartData = {
    labels: data.map(d => d.campaign_id),
    datasets: [
      {
        label: 'Ad Spend ($)',
        data: data.map(d => d.spend),
        backgroundColor: '#8B5CF6',
        borderRadius: 4,
      },
      {
        label: 'CPA ($)',
        data: data.map(d => d.cost_per_acquisition),
        backgroundColor: '#F59E0B',
        borderRadius: 4,
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { color: '#F8FAFC' } },
    },
    scales: {
      y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#94A3B8' } },
      x: { grid: { display: false }, ticks: { color: '#94A3B8' } },
    }
  };

  return (
    <div className="dashboard-grid grid-cols-1">
      <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '24px' }}>Marketing & Campaign ROI</h2>
      
      <div className="glass-card" style={{ height: '400px' }}>
        <Bar data={chartData} options={chartOptions} />
      </div>

      <div className="glass-card mt-lg">
        <h3 className="card-title">Campaign Performance Ranking</h3>
        <div style={{ overflowX: 'auto' }} className="mt-md">
          <table className="data-table">
            <thead>
              <tr>
                <th>Campaign ID</th>
                <th>Spend</th>
                <th>Clicks</th>
                <th>Conversions</th>
                <th>Conv. Rate</th>
                <th>CPA</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 500, color: '#F8FAFC' }}>{row.campaign_id}</td>
                  <td>${row.spend.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                  <td>{row.clicks.toLocaleString()}</td>
                  <td>{row.conversions.toLocaleString()}</td>
                  <td className={row.conv_rate > 0.1 ? 'text-success' : ''}>{(row.conv_rate * 100).toFixed(2)}%</td>
                  <td>${row.cost_per_acquisition.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
