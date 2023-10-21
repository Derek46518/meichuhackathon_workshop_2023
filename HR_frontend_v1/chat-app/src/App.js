import React from 'react';
import ChatBox from './hr_chatbox/ChatBox';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DashboardApp from './hr_dashboard/DashboardApp';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/hr_dashboard/DashboardApp" element={<DashboardApp />} />
          <Route path="/" element={<ChatBox />} />
        </Routes>
      </Router>
    </div>
  );
}
/*
function App() {
  return (
    <div className="App">
      <ChatBox />
    </div>
  );
}
*/
export default App;