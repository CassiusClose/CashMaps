import React from 'react';

export default class LoadingTextAnim extends React.Component {
  constructor(props) {
    super(props);

    this.state = {text: "Loading.", num_periods: 1, anim_delay: props.speed, timer_id: null};

  }

  componentDidMount() {
    var self = this;
    var id = setInterval(function () {
      self.updateLoadingText();
    }, this.state.anim_delay);
    this.setState({timer_id: id});
  }

  updateLoadingText() {
    var periods = this.state.num_periods;
    periods += 1;
    if(periods > 3) {
      periods = 1;
    }
  
    var text = "Loading";
    for(var i = 0; i < periods; i++) {
      text += ".";
    }

    this.setState({text: text, num_periods: periods});
  }

  componentWillUnmount() {
    clearInterval(this.state.timer_id);
  }

  render() {
    return(
      <div>
        <h1>
          {this.state.text}
        </h1>
      </div>
    );
  }
}

LoadingTextAnim.defaultProps = {speed: 500};
