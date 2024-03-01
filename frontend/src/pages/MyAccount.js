import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect } from 'react';

const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)

    useEffect(() => {
        const fetchUserRoutes = async () => {
            try {
                const response = await fetch('/api/userroutes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }),
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log(data)
            } catch (error) {
                console.error('There was a problem with your fetch operation:', error);
            }
        };

        fetchUserRoutes();
    }, []);

    return (
        <div className='MyAccount'>
            <Header />
            <h2>My Account Page</h2>
            <h3>Username: {username}</h3>
        </div>
    );
};

export default MyAccount;