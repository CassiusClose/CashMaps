import React from 'react';
import ReactDOM from 'react-dom';
import routes from './routes';
import { Viewer } from 'resium';

class Test extends React.Component {
  render() {
    return(
      <Viewer />
    );
  }
}

ReactDOM.render(<Test />, document.getElementById('root'));
