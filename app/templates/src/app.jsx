import React from 'react';
import { Router, Route } from 'react-router-dom';
import history from "./history";

import IndexPage from "./pages/indexPage";
import FilePage from "./pages/filePage";
import Header from "./pages/header";
import ParserPage from "./pages/parserPage";
import MapPage from "./pages/mapPage";
import UploadPage from "./pages/uploadPage";
import PhotosPage from "./pages/photosPage";
import ToolsPage from "./pages/toolsPage";
import SocketPage from "./pages/socketPage";

/*Uses the react-router plugin to route to different pages depending on the current URL.*/

export default (
  <Router history={history}>
    <div>
      <Header />
      <Route exact={true} path='/' component={IndexPage} />
      <Route path='/files' component={FilePage} />
      <Route path='/parser' component={ParserPage} />
      <Route path='/map' component={MapPage} />
      <Route path='/upload' component={UploadPage} />
      <Route path='/gallery' component={PhotosPage} />
      <Route path='/tools' component={ToolsPage} />
      <Route path='/notifications' component={SocketPage} />
    </div>
  </Router>
);
