import React from 'react';
import "./progressBar.css";

export default function ProgressBar(props) {
    return(
      <div className="ProgressBar_Div">
        <progress
          className="ProgressBar_Progress"
          value={this.props.progress}
          max={this.props.max}
        />
        <div className="ProgressBar_Message">
          {this.props.message != null && this.props.message}
        </div>
      </div>
    );
}
