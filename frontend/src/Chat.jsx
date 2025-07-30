import React, { useEffect, useState, useRef } from 'react';

function Chat({ roomName }) {
  const [messages, setMessages] = useState([]);
  const [value, setValue] = useState('');
  const socketRef = useRef(null);

  useEffect(() => {
    // WebSocket connection
    socketRef.current = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/`);

    socketRef.current.onmessage = e => {
      const data = JSON.parse(e.data);
      setMessages(prev => [...prev, { message: data.message, username: data.username }]);
    };

    // Fetch old messages
    fetch(`http://127.0.0.1:8000/api/messages/${roomName}/`)
      .then(res => res.json())
      .then(data => {
        const loaded = data.map(msg => ({
          message: msg.content,
          username: msg.username,
        }));
        setMessages(loaded);
      });

    return () => socketRef.current.close();
  }, [roomName]);

  const sendMessage = () => {
  if (
    socketRef.current &&
    socketRef.current.readyState === WebSocket.OPEN
  ) {
    socketRef.current.send(JSON.stringify({
      message: value,
      username: 'GuestUser',
    }));
    setValue('');
  } else {
    console.warn("WebSocket is not open.");
    alert("Chat connection lost. Please refresh the page.");
  }
};

  return (
    <div>
      <h2>Room: {roomName}</h2>
      <div style={{ height: '200px', overflowY: 'auto', border: '1px solid gray' }}>
        {messages.map((msg, idx) => (
          <p key={idx}><strong>{msg.username}:</strong> {msg.message}</p>
        ))}
      </div>
      <input value={value} onChange={e => setValue(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chat;
