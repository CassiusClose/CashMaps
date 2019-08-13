import React from 'react';

export default function FlashedMessages(props) {
  return(
    <div>
      <h2>Notifications</h2>
      <ul>
        {
          props.flashedMessages != null &&
          props.flashedMessages.map((item) => (
            <li key={item.id}>{item.message}</li>
          ))
        }
      </ul>
    </div>
  );
}
