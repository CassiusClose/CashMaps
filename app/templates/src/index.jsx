import ReactDOM from 'react-dom';
import routes from './routes';

/* This file is the entry point for webpack. That is, this is the file it will start with when
 * finding which files to bundle. Any files linked here will be included.
 *
 * This renders the HTML in the routes files, which links to certain pages based on the URL.
 */

ReactDOM.render(routes, document.getElementById('root'));
