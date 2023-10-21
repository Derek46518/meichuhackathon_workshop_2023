import React from 'react';
import ChatBox from './hr_chatbox/ChatBox';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DashboardApp from './hr_dashboard/DashboardApp';
import Select_role from './select_role_page/Select_role';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Select_role />} />
          <Route path="/hr_dashboard/DashboardApp" element={<DashboardApp />} />
          <Route path="/hr_chatbox/ChatBox" element={<ChatBox />} />
        </Routes>
      </Router>
    </div>
  );
}
export default App;