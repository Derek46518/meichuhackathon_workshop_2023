import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function Dashboard({ title, data }) {
  const date = Object.keys(data);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h2>{title}</h2>
      <LineChart width={500} height={300} data={data}>
        <XAxis dataKey='date' />
        <YAxis />
        <CartesianGrid strokeDasharray="3 3" />
        <Tooltip />
        <Legend wrapperStyle={{ margin: '55px', right:'75px', left:'0px' }} />
        <Line type="monotone" dataKey="HQ" stroke="#8884d8" />
        <Line type="monotone" dataKey="AZ" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
}

export default Dashboard;
