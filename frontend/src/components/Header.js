import React from 'react';

const Header = ({ isLoggedIn }) => {
    return (
        <div className="Header">
            <nav class="navbar bg-body-tertiary">
                <div class="container-fluid">
                    <div class="d-flex">
                        <div class="dropdown">
                            <button class="navbar-toggler" type="button" data-bs-toggle="dropdown" aria-expanded="false"><span class="navbar-toggler-icon"></span></button>
                            <ul class="dropdown-menu">
                                <li><button class="dropdown-item" type="button">Menu1</button></li>
                                <li><button class="dropdown-item" type="button">Menu2</button></li>
                                <li><button class="dropdown-item" type="button">Menu3</button></li>
                            </ul>
                        </div>
                        <a class="navbar-brand ms-2" href="/">PathPal</a>
                    </div>
                    <div class="d-flex">
                    {isLoggedIn ? (
                            <a className="btn btn-info text-white me-2" type="submit" href="/my-account">My Account</a>
                        ) : (
                            <span>
                                <a className="btn btn-outline-success me-2" type="submit" href="/sign-up">Sign Up</a>
                                <a className="btn btn-outline-success" type="submit" href="/login">Login</a>
                            </span>
                        )}
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Header;