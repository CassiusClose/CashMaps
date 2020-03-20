import React, { useState } from 'react';

export default function ToolsPage(props) {
  const removeTracks = () => {
    $.ajax({
      url: "/map/_clear_data",
      type: "POST",
      success: function(response) {
        console.log("Cleared tracks"); 
      }
    });
  }

  const clearRQ = () => {
    $.ajax({
      url: "/_clear_rq",
      type: "POST",
      success: function(response) {
        console.log("Cleared Redis Queue");
      }
    });
  }

  return(
    <div>
      <button onClick={removeTracks}>Remove Tracks</button>
      <button onClick={clearRQ}>Clear Redis Queue</button>
    </div>
  );
}
