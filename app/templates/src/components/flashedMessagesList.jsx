import React, { useState, useEffect } from 'react';

export default function FlashedMessages(props) {
  const [messages, setMessages] = useState(null);

  useEffect(() => {
    if(props.url) {
      var scheduler = setTimeout(() => {
        $.ajax({
          url: '/parser/_get_flashed_messages',
          type: 'POST',
          success: function(response) {
            console.log(response.messages);
            if(!messages) {
              setMessages(response.messages);
            }
            else if(response.messages) { 
              setMessages(messages.concat(response.messages));
            }
          }
        });
      }, props.FETCH_DELAY);
    }

    return () => {
      clearTimeout(scheduler);
    }
  });

  return(
    <div>
      <h2>Notifications</h2>
      <ul>
        {
          messages != null &&
          messages.map((item) => (
            <li key={item.id}>{item.message}</li>
          ))
        }
      </ul>
    </div>
  );
}

FlashedMessages.defaultProps = { FETCH_DELAY: 500 };
