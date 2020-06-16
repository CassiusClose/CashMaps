import ReactDOM from 'react-dom';
import app from './app';
import io from 'socket.io-client';


/* This file is the entry point for webpack. That is, this is the file it will start with when
 * finding which files to bundle. Any files linked here will be included.
 *
 * This renders the HTML in the routes files, which links to certain pages based on the URL.
 */

ReactDOM.render(app, document.getElementById('root'));
