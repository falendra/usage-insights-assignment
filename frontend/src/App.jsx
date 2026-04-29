import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import './App.css';

function App() {
  const [data, setData] = useState({
    daily_usage: [],
    feature_usage: [],
    team_usage: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Assuming Django is running on port 8000
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/usage/?account_id=1');
        
        // Clean up team__name for Recharts (handle null teams)
        const formattedTeamUsage = response.data.team_usage.map(item => ({
          ...item,
          team__name: item.team__name || 'No Team'
        }));
        
        setData({
          ...response.data,
          team_usage: formattedTeamUsage
        });
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch usage data. Make sure the Django backend is running on port 8000 and has data.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Usage Insights Dashboard</h1>
        <p>Account Overview</p>
      </header>

      <div className="charts-grid">
        <div className="chart-card full-width">
          <h2>Daily Usage</h2>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.daily_usage} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total" name="Total Events" stroke="#8884d8" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <h2>Feature Usage</h2>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.feature_usage} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="feature_name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total" name="Total Events" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <h2>Team Usage</h2>
          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.team_usage} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="team__name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total" name="Total Events" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
