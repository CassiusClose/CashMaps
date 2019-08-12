import React from 'react';
import history from '../history';
import { Link } from 'react-router-dom';

export default class Header extends React.Component {
  redirect(path) {
    console.log(path);
    if(path == window.location.pathname) {
      history.push('/'); 
      history.push(path);
    }
    else {
      history.push(path);
    }
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
        <hr/>
      </div>
    );
  }
n}
