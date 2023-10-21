import React from 'react';
import ChatBox from './hr_chatbox/ChatBox';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DashboardApp from './hr_dashboard/DashboardApp';
import Select_role from './select_role_page/Select_role';
import Report_scan from './security_chatbox/Report_scan'

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Select_role />} />
          <Route path="/hr_chatbox/ChatBox" element={<ChatBox />} />
          <Route path="/security_chatbox/Report_scan" element={<Report_scan />} />
          <Route path="/hr_dashboard/DashboardApp" element={<DashboardApp />} />
        </Routes>
      </Router>
    </div>
  );
}
export default App;