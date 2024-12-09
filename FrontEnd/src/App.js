import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import CreateBuild from './components/CreateBuild';
import FilterParts from './components/FilterParts';
import CompareParts from './components/CompareParts';

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/create" component={CreateBuild} />
          <Route path="/filter" component={FilterParts} />
          <Route path="/compare" component={CompareParts} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
