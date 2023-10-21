import React from 'react';
import './message.css';

function Message({ user, text }) {
  return (
    <div className={`message ${user === 'user' ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">{text}</div>
    </div>
  );
}

export default Message;
