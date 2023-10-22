import React, { useState } from 'react';
import axios from 'axios';
import './ChatInput.css';

function ChatInput({ onSendMessage }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // 构建API请求的URL
    const apiUrl = 'https://localhost:5000/robotResponse'; // 替换成你的API的URL

    // 构建请求数据
    const requestData = { message }; // 这里使用message作为请求的数据

    // 发送POST请求
    axios.get(apiUrl+'/'+requestData)
      .then(response => {
        // 请求成功时的处理
        console.log(response.data); // 根据API的响应进行处理
        onSendMessage(message);
        setMessage('');
      })
      .catch(error => {
        // 请求失败时的处理
        console.error('Error:', error);
      });
      
  };

/*
function ChatInput({ onSendMessage }) {
  const [message, setMessage] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSendMessage(message);
    setMessage('');
  };
*/
  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default ChatInput;
    