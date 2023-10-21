import React, { useState } from 'react';
import axios from 'axios';
import './Report_scan.css';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';


function ReportScan() {
    const [report, setReport] = useState(null);
    const [maintenancePredictions, setMaintenancePredictions] = useState([]);
    const [loading, setLoading] = useState(false);
  
    const fetchReport = async () => {
      setLoading(true);
      try {
        const reportResponse = await axios.get('/api/report');
        const maintenanceResponse = await axios.get('/api/maintenance-predictions');
        setReport(reportResponse.data);
        setMaintenancePredictions(maintenanceResponse.data);
      } catch (error) {
        console.error('Error fetching data from backend', error);
      }
      setLoading(false);
    };
  
    return (
      <div className="App">
      <div className="report-section">
        <div className="svg-image">
          <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 32 32"><path fill="currentColor" d="M11 21H9v-2a3.003 3.003 0 0 1 3-3h6v2h-6a1.001 1.001 0 0 0-1 1zm4-6a4 4 0 1 1 4-4a4.005 4.005 0 0 1-4 4zm0-6a2 2 0 1 0 2 2a2.002 2.002 0 0 0-2-2zm9 13a4 4 0 1 1 4-4a4.005 4.005 0 0 1-4 4zm0-6a2 2 0 1 0 2 2a2.002 2.002 0 0 0-2-2zm6 12h-2v-2a1.001 1.001 0 0 0-1-1h-6a1.001 1.001 0 0 0-1 1v2h-2v-2a3.003 3.003 0 0 1 3-3h6a3.003 3.003 0 0 1 3 3z"/><path fill="currentColor" d="m14 27.733l-5.234-2.79A8.986 8.986 0 0 1 4 17V4h20v6h2V4a2.002 2.002 0 0 0-2-2H4a2.002 2.002 0 0 0-2 2v13a10.981 10.981 0 0 0 5.824 9.707L14 30Z"/></svg>
        </div>
        <Button variant="contained" color="primary" onClick={fetchReport} disabled={loading}>
          {loading ? <CircularProgress size={24} /> : 'Fetch Report'}
        </Button>
        {report && (
          <Paper elevation={3} className="report">
            <Typography variant="body1">{report}</Typography>
          </Paper>
        )}
      </div>
  
        <div className="maintenance-section">

        </div>
      </div>
    );
}

export default ReportScan;
