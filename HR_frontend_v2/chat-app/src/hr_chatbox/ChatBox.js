import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Message from './message';
import ChatInput from './ChatInput';
import ChatMenu from './ChatMenu';
import './ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
/*
  const [options, setOptions] = useState([
    //{ label: 'Option 1', value: 'option1' },
    //{ label: 'Option 2', value: 'option2' },
    // ...更多選項
  ]);
*/
  const handleSendMessage = (text) => {
    setMessages([...messages, { user: 'user', text }]);
    // 在這裡你可以添加對 bot 的回應
  };
/*
  const handleSelectOption = (option) => {
    setMessages([...messages, { user: 'user', text: option.label }]);
    // 在這裡處理選單選項被選擇的邏輯
  };
*/
  return (
    <div className="chat-box">
      <div className="chat-header">
        人資主管對話介面
      </div>
      <div className="messages">
        {messages.map((message, index) => (
          <Message key={index} user={message.user} text={message.text} />
        ))}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
      <Link to="../hr_dashboard/dashboardApp" className="dashboard-button">
        前往 Dashboard
      </Link>
    </div>

    
  );


}

export default ChatBox;
