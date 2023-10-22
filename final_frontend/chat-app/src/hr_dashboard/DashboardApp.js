import React, { useState, useEffect } from 'react';
import Dashboard from './Dashboard';
import DatePicker from './DatePicker';
import './Dashboard.css'

function DashboardApp() {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [dailyData, setDailyData] = useState([]);
  const [weeklyData, setWeeklyData] = useState([]);
  const getDailyURL = 'http://localhost:5000/getDaily/'+date
  const getWeeklyURL = 'http://localhost:5000/getWeekly/'+date
  useEffect(() => {
    // 获取REST API数据
    fetch(getDailyURL)
      .then(response => response.json())
      .then(data => {
        const transformedData = Object.keys(data).map(key => {
          const deptName = key;
          const HQValue = data[key]["HQ"];
          const AZValue = data[key]["AZ"];
        
          return { date: deptName, HQ: HQValue, AZ: AZValue };
        });

        // console.log(Object.values(transformedData))
        setDailyData(Object.values(transformedData)); // 更新dailyData状态
      })
      .catch(error => {
        console.error('获取数据时出错：', error);
      });

    // 获取REST API数据
    fetch(getWeeklyURL)
      .then(response => response.json())
      .then(data => {
        const transformedData = Object.keys(data).map(key => {
          const deptName = key;
          const HQValue = data[key]["HQ"];
          const AZValue = data[key]["AZ"];
        
          return { date: deptName, HQ: HQValue, AZ: AZValue };
        });
        // console.alert(JSON.stringify(transformedData ))
        setWeeklyData(Object.values(transformedData)); // 更新weeklyData状态
      })
      .catch(error => {
        console.error('获取数据时出错：', error);
      });
  }, [date]);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Employees Arrival Dashboard</h1>
      <DatePicker onDateChange={setDate} />
      <div className="chart-container">
        <Dashboard title="Daily Arrival Rate" data={dailyData} />
      </div>
      <div className="chart-container">
        <Dashboard title="Weekly Arrival Rate" data={weeklyData} />
      </div>
    </div>
  );
}

export default DashboardApp;