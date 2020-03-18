import React from 'react';
import Animated from 'react-native';

export default class LoadingTextAnim extends React.Component {
  constructor(props) {
    super(props);

    this.state = {text: "Loading.", periods: new Animated.Value(0)};

    React.useEffect(() => {
      Animated.timing(

      )

    }, [])
  }

  render() {
    <div>
      <h1>
        {this.state.text}
      </h1>
    </div>
  }
}
