import React from 'react';
import history from '../history';
import { Link } from 'react-router-dom';
import './header.css';

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
      <div className="Header_Container">
        <div className="Header_Links">
          <button onClick={() => this.redirect('/')}>Home</button>
          <button onClick={() => this.redirect('/parser')}>Parsers</button>
          <button onClick={() => this.redirect('/map')}>Map</button>
          <button onClick={() => this.redirect('/upload')}>Upload</button>
          <button onClick={() => this.redirect('/gallery')}>Gallery</button>
        </div>
        <hr/>
      </div>
    );
  }
}
//Hidden links
          <button onClick={() => this.redirect('/files')}>Files</button>
