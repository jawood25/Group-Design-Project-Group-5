import React from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

const Header = () => {
    const isLoggedIn = useSelector((state) => state.loginStatus.isLoggedIn);
    return (
        <div className="Header">
            <nav className="navbar bg-body-tertiary" style={{ height: "80px" }}>
                <div className="container-fluid">
                    <div className="d-flex">
                        <div className="dropdown align-items-center">
                            <button className="navbar-toggler" type="button" data-bs-toggle="dropdown" aria-expanded="false"><span className="navbar-toggler-icon"></span></button>
                            <ul className="dropdown-menu">
                                <li><Link to="/upload-route" className="dropdown-item">Mapbox Upload Route</Link></li>
                                <li><Link to="/community" className="dropdown-item">Community</Link></li>
                            </ul>
                        </div>
                        <Link to="/" className="navbar-brand ms-2" style={{fontSize: "1.7rem"}}>PathPal</Link>
                    </div>
                    <div className="d-flex">
                    {isLoggedIn ? (
                            <Link to="/my-account" className="btn btn-info text-white me-2 btn-lg">My Account</Link>
                        ) : (
                            <span>
                                <Link to="/sign-up" className="btn btn-outline-success me-2 btn-lg">Sign Up</Link>
                                <Link to="/login" className="btn btn-outline-success btn-lg">Login</Link>
                            </span>
                        )}
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Header;