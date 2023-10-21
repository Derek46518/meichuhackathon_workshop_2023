import React from 'react';
import './Select_role.css';
import { Button, Space } from 'antd';
import { useNavigate } from 'react-router-dom';

function SelectRole() {
  const handleRedirect = (url) => {
    window.location.href = url;
  };

  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="container">
      <div className="box">
      <svg xmlns="http://www.w3.org/2000/svg" width="10em" height="10em" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 13a4 4 0 1 0 0-8a4 4 0 0 0 0 8Zm-6 9v-3a6 6 0 1 1 12 0v3M13 5c.404-1.664 2.015-3 4-3c2.172 0 3.98 1.79 4 4c-.02 2.21-1.828 4-4 4h-1h1c3.288 0 6 2.686 6 6v2M11 5c-.404-1.664-2.015-3-4-3c-2.172 0-3.98 1.79-4 4c.02 2.21 1.828 4 4 4h1h-1c-3.288 0-6 2.686-6 6v2"/></svg>
        <h2>人力資源</h2>
        <Button type="primary" onClick={() => handleNavigate('../hr_chatbox/Chatbox')}>前往</Button>
      </div>
      <div className="text">Who are you?</div>
      <div className="box">
      <svg xmlns="http://www.w3.org/2000/svg" width="10em" height="10em" viewBox="0 0 24 24"><path fill="currentColor" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12c5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>        <h2>資訊保護與維安</h2>
        <Button type="primary" onClick={() => handleRedirect('https://example.com/page1')}>前往</Button>
      </div>
    </div>
  );
}

export default SelectRole;