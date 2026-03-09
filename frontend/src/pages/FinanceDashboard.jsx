import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export default function FinanceDashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/kpis/finance-monthly');
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
    labels: data.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`),
    datasets: [
      {
        label: 'Revenue',
        data: data.map(d => d.revenue),
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      },
      {
        label: 'Net Profit',
        data: data.map(d => d.net_profit),
        borderColor: '#10B981',
        backgroundColor: 'transparent',
        borderDash: [5, 5],
        tension: 0.4,
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
      <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '24px' }}>Financial Performance</h2>
      
      <div className="glass-card" style={{ height: '400px' }}>
        <Line data={chartData} options={chartOptions} />
      </div>

      <div className="glass-card mt-lg">
        <h3 className="card-title">Monthly Breakdown</h3>
        <div style={{ overflowX: 'auto' }} className="mt-md">
          <table className="data-table">
            <thead>
              <tr>
                <th>Period</th>
                <th>Revenue</th>
                <th>Net Profit</th>
                <th>Margin</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.year}-{String(row.month).padStart(2, '0')}</td>
                  <td>${row.revenue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                  <td>${row.net_profit.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                  <td>{((row.net_profit / row.revenue) * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
