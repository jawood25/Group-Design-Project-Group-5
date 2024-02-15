import React from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

const Header = () => {
    const isLoggedIn = useSelector((state) => state.loginStaus.isLoggedIn);
    return (
        <div className="Header">
            <nav className="navbar bg-body-tertiary">
                <div className="container-fluid">
                    <div className="d-flex">
                        <div className="dropdown">
                            <button className="navbar-toggler" type="button" data-bs-toggle="dropdown" aria-expanded="false"><span className="navbar-toggler-icon"></span></button>
                            <ul className="dropdown-menu">
                                <li><button className="dropdown-item" type="button">Menu1</button></li>
                                <li><button className="dropdown-item" type="button">Menu2</button></li>
                                <li><button className="dropdown-item" type="button">Menu3</button></li>
                            </ul>
                        </div>
                        <Link to="/" className="navbar-brand ms-2">PathPal</Link>
                    </div>
                    <div className="d-flex">
                    {isLoggedIn ? (
                            <Link to="/my-account" className="btn btn-info text-white me-2">My Account</Link>
                        ) : (
                            <span>
                                <Link to="/sign-up" className="btn btn-outline-success me-2">Sign Up</Link>
                                <Link to="/login" className="btn btn-outline-success">Login</Link>
                            </span>
                        )}
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Header;