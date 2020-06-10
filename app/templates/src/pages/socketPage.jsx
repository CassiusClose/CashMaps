import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000')

export default function socketPage(props) {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    socket.on('message', (data) => {
      var copy = [...messages];
      copy.push(data.message);
      setMessages(messages => [...messages,data]);
    });
  }, []);
  
  const emitMessage = (e) => {
    socket.emit(
      'send_message',
      {
        body: 'message sent',
        timestamp: Date.now()
      }
    );
  }

  return(
    <div>
      <h1>Socket Messages</h1>
      <button onClick={ emitMessage }>Emit</button>
        { messages != null &&
          messages.map((item) => {
            return(<p key={item.message}>Message: {item.message}</p>);
          })
        }
    </div>
  );
}
