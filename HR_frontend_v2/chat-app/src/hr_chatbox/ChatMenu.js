import React from 'react';
import './ChatMenu.css';

function ChatMenu({ options, onSelect }) {
  return (
    <div className="chat-menu">
      {options.map((option, index) => (
        <button key={index} onClick={() => onSelect(option)}>
          {option.label}
        </button>
      ))}
    </div>
  );
}

export default ChatMenu;
