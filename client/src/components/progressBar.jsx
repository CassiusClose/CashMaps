import React from 'react';
import "./progressBar.css";

export default function ProgressBar(props) {
    return(
      <div className="ProgressBar_Div">
        <progress
          className="ProgressBar_Progress"
          value={props.progress}
          max={props.max}
        />
        <div className="ProgressBar_Message">
          {props.message != null && props.message}
        </div>
      </div>
    );
}
