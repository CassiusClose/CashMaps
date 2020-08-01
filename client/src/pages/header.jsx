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
        <button name="about" onClick={() => redirect('/')}>About</button>
        <button name="parser" onClick={() => redirect('/parser')}>Parsers</button>
        <button name="map" onClick={() => redirect('/map')}>Map</button>
        <button name="tools" onClick={() => redirect('/tools')}>Tools</button>
      </div>
      <hr/>
    </div>
  );
}

//Hidden links
//<button onClick={() => redirect('/files')}>Files</button>
//<button onClick={() => redirect('/upload')}>Upload</button>
//<button onClick={() => redirect('/gallery')}>Gallery</button>
