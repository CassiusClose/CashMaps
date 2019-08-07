import React from 'react';
import { Router, Route } from 'react-router-dom';
import history from "./history";

import IndexPage from "./pages/indexPage";
import FilePage from "./pages/filePage";
import Header from "./pages/header";
import CesiumMap from "./pages/cesiumMap";

export default (
  <Router history={history}>
    <div>
      <Header />
      <Route exact={true} path='/' component={IndexPage} />
      <Route path='/files' component={FilePage} />
      <Route path='/map' component={CesiumMap} />
    </div>
  </Router>
);