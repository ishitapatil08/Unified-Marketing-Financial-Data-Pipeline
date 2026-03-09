import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, DollarSign } from 'lucide-react';
import ExecutiveSummary from './pages/ExecutiveSummary';
import FinanceDashboard from './pages/FinanceDashboard';
import MarketingDashboard from './pages/MarketingDashboard';

function Sidebar() {
  const location = useLocation();
  const getNavClass = (path) => {
    return `nav-item ${location.pathname === path ? 'active' : ''}`;
  };

  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">IF</div>
        <span>IntelligencePlatform</span>
      </div>
      <nav className="sidebar-nav">
        <Link to="/" className={getNavClass('/')}>
          <LayoutDashboard size={20} />
          Executive Summary
        </Link>
        <Link to="/finance" className={getNavClass('/finance')}>
          <DollarSign size={20} />
          Finance Dashboard
        </Link>
        <Link to="/marketing" className={getNavClass('/marketing')}>
          <TrendingUp size={20} />
          Marketing Dashboard
        </Link>
      </nav>
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="avatar" />
          <div className="user-details">
            <span className="user-name">Local Admin</span>
            <span className="user-role">Analyst</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <header className="topbar">
            <h1>Integrated Analytics</h1>
            <div className="global-actions">
              <button className="btn btn-primary">Export Report</button>
            </div>
          </header>
          <div className="content-area">
            <Routes>
              <Route path="/" element={<ExecutiveSummary />} />
              <Route path="/finance" element={<FinanceDashboard />} />
              <Route path="/marketing" element={<MarketingDashboard />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
