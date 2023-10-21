import React from 'react';

function DatePicker({ onDateChange }) {
  return (
    <div className="date-picker-container">
      <label className="date-picker-label">Choose date:</label>
      <input type="date" onChange={(e) => onDateChange(e.target.value)} className="date-picker-input" />
    </div>
  );
}

export default DatePicker;
