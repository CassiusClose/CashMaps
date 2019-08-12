import React from 'react';

export default class ProgressBar extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return(
      <div>
        <progress value={this.props.progress} max={this.props.max} />
        {this.props.message != null && this.props.message}
      </div>
    );
  }
}
