import React, { useState, useEffect } from 'react';
import { socket_notifications } from './../sockets';

export default function NotificationsList(props) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket_notifications.on(props.notification_name, (data) => {
      if(data.timestamp != null && data.message != null)
        setMessages(messages => [...messages, data]);
    });
  }, []);

  return(
    <div>
      <h2>Notifications</h2>
      <ul>
        { messages != null &&
          messages.map((item) => (
            <li key={item.timestamp}>{item.message}</li>
          ))
        }
      </ul>
    </div>
  );
}

