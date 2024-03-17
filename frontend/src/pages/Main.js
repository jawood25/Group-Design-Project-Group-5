import Header from '../components/Header';
import MainMap from '../components/MainMap';
import React, { useEffect, useState } from 'react';
import RouteSearch from '../components/RouteSearch';

const Main = () => {
    const [allUR, setAllUR] = useState(null);

    const handleSearch = async (searchParams) => {
        try {
            const response = await fetch('/api/searchroute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchParams),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            setAllUR(data.routes);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

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
                console.log(data.routes);
                setAllUR(data.routes)
            } catch (error) {
                console.error('There was a problem with your fetch operation:', error);
            }
        };

        fetchUserRoutes();
    }, []);

    return (
        <div className='Main'>
            <Header />
            <RouteSearch onSearch={handleSearch} />
            <MainMap allUR={allUR}/>
        </div>
    );
};

export default Main;