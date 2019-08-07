import React from 'react';
import history from '../history';

export default class Header extends React.Component {
  redirect(path) {
    history.push(path);
  }

  render() {
    return(
      <div>
        <div>
          <button onClick={() => this.redirect('/')}>Home</button>
          <button onClick={() => this.redirect('/files')}>Files</button>
          <button onClick={() => this.redirect('/parser')}>Parsers</button>
          <button onClick={() => this.redirect('/map')}>Map</button>
        </div>
        <hr></hr>
      </div>
    );
  }
}
