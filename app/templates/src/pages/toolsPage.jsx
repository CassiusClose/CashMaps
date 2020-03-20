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

  const clearParseTasks = () => {
    $.ajax({
      url: "/parser/_clear_nonactive_tasks",
      type: "POST",
      success: function(response) {
        console.log("Cleared parse tasks");
      }
    });
  }

  return(
    <div>
      <button onClick={removeTracks}>Remove Tracks</button>
    </div>
  );
}
      //<button onClick={clearParseTasks}>Clear Nonactive Parse Tasks</button>
