import React from 'react';

function DatePicker({ onDateChange }) {
  return (
    <div>
      <label>chose date:</label>
      <input type="date" onChange={(e) => onDateChange(e.target.value)} />
    </div>
  );
}

export default DatePicker;
