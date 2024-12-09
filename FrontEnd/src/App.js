import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar';
import ComponentDetails from './components/ComponentDetails';
import FilterParts from './components/FilterParts';
import CompareParts from './components/CompareParts';

function App() {
    return (
        <Router>
            <NavBar />
            <Switch>
                <Route path="/filter/:componentType" render={({ match }) => (
                    <FilterParts componentType={match.params.componentType} />
                )} />
                <Route path="/compare/:componentType" render={({ match }) => (
                    <CompareParts componentType={match.params.componentType} />
                )} />
                <Route path="/details/:componentType/:id" component={ComponentDetails} />
                <Route path="/" exact render={() => <h1>Welcome to the PC Builder App</h1>} />
            </Switch>
        </Router>
    );
}

export default App;
