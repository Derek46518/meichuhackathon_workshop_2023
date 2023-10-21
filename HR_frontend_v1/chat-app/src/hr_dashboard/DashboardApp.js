import React, { useState, useEffect } from 'react';
import Dashboard from './Dashboard';
import DatePicker from './DatePicker';

function DashboardApp() {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [dailyData, setDailyData] = useState([]);
  const [weeklyData, setWeeklyData] = useState([]);

  useEffect(() => {
    // 後端要給這裡資料
    setDailyData([
      // Example data
      { date: 'Dept1', HQ: 80, AZ: 70 },
      { date: 'Dept2', HQ: 85, AZ: 65 },
      { date: 'Dept3', HQ: 80, AZ: 70 },
      { date: 'Dept4', HQ: 85, AZ: 65 },
    ]);

    // 後端要給這裡資料
    setWeeklyData([
      { date: 'Monday', HQ: 80, AZ: 70 },
      { date: 'Tuesday', HQ: 85, AZ: 65 },
      { date: 'Wednesday', HQ: 90, AZ: 60 },
      { date: 'Thursday', HQ: 95, AZ: 55 },
      { date: 'Friday', HQ: 100, AZ: 50 },
    ]);
  }, [date]);

  return (
    <div>
      <h1>Employees Arrival Dashboard</h1>
      <DatePicker onDateChange={setDate} />
      <Dashboard title="Dately Arrival Rate" data={dailyData} />
      <Dashboard title="Weekly Arrival Rate" data={weeklyData} />
    </div>
  );
}

export default DashboardApp;
