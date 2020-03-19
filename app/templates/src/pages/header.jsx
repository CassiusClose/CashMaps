import React from 'react';
import history from '../history';
import { Link } from 'react-router-dom';
import './header.css';

/**
 * This component is the header above all the content on the webpage that links to different
 * parts of the website. routes.jsx will display this on every page.
 */
export default function Header(props) {
  const redirect = (path) => {
    history.push(path);
  }

  return(
    <div className="Header_Container">
      <div className="Header_Links">
        <button onClick={() => redirect('/')}>About</button>
        <button onClick={() => redirect('/parser')}>Parsers</button>
        <button onClick={() => redirect('/map')}>Map</button>
        <button onClick={() => redirect('/upload')}>Upload</button>
        <button onClick={() => redirect('/gallery')}>Gallery</button>
        <button onClick={() => redirect('/tools')}>Tools</button>
      </div>
      <hr/>
    </div>
  );
}

//Hidden links
        <button onClick={() => redirect('/files')}>Files</button>
