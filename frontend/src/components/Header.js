import React from 'react';

const Header = () => {
    return (
        <div className="Header">
            <nav class="navbar bg-body-tertiary">
                <div class="container-fluid">
                    <div class="dropdown">
                        <button class="navbar-toggler" type="button" data-bs-toggle="dropdown" aria-expanded="false"><span class="navbar-toggler-icon"></span></button>
                        <ul class="dropdown-menu">
                            <li><button class="dropdown-item" type="button">Menu1</button></li>
                            <li><button class="dropdown-item" type="button">Menu2</button></li>
                            <li><button class="dropdown-item" type="button">Menu3</button></li>
                        </ul>
                    </div>
                    <a class="navbar-brand" href="/">PathPal</a>
                    <div class="d-flex">
                        <a class="btn btn-outline-success me-2" type="submit" href="/sign-up">Sign Up</a>
                        <a class="btn btn-outline-success" type="submit" href="/login">Login</a>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Header;