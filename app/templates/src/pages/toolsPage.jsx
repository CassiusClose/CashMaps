import React, { useState } from 'react';

export default function ToolsPage(props) {
  const removeTracks = () => {
    $.ajax({
      url: "/map/_clear_data",
      type: "POST",
      success: function(response) {
        console.log("Cleared"); 
      }
    });
  }

  return(
    <div>
      <button onClick={removeTracks}>Remove Tracks</button>
    </div>
  );
}
