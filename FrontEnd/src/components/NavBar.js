import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/create">Create Build</Link></li>
                <li><Link to="/filter">Filter Parts</Link></li>
                <li><Link to="/compare">Compare Parts</Link></li>
            </ul>
        </nav>
    );
}

export default NavBar;
