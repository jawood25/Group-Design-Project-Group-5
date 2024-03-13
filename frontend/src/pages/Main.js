import Header from '../components/Header';
import MainMap from '../components/MainMap';
import React, { useEffect, useState } from 'react';

const Main = () => {
    const [allUR, setAllUR] = useState(null);
    useEffect(() => {
        const fetchUserRoutes = async () => {
            try {
                const response = await fetch('/api/allUR', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setAllUR(data.user_routes)
            } catch (error) {
                console.error('There was a problem with your fetch operation:', error);
            }
        };

        fetchUserRoutes();
    }, []);

    return (
        <div className='Main'>
            <Header />
            <MainMap allUR={allUR}/>
        </div>
    );
};

export default Main;