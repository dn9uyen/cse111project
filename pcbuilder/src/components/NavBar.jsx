import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/filter/cpu">Filter Parts</Link></li>
                <li><Link to="/compare/cpu">Compare Parts</Link></li>
            </ul>
        </nav>
    );
}

export default NavBar;
