import React from 'react';
import history from '../history';
import { Link } from 'react-router-dom';

/**
 * This class is the header above all the content on the webpage that links to different
 * parts of the website. routes.jsx will display this on every page.
 */
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
        <hr/>
      </div>
    );
  }
n}
