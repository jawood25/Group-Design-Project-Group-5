import React, { useState, useEffect } from 'react';
import Header from '../components/Header';

const Main = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(true);

    const checkLoginStatus = async () => {
        try {
            const response = await fetch('/api/check-login-status');
            if (response.ok) {
                const data = await response.json();
                setIsLoggedIn(data.isLoggedIn);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    
    useEffect(() => {
        checkLoginStatus();
    }, []);

    return (
        <div className='Main'>
            <Header isLoggedIn={isLoggedIn} />
            <h2>Main Page</h2>
        </div>
    );
};

export default Main;