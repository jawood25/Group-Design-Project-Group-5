import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import MapboxRenderLine from './MapboxRenderLine';

const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)
    const [routeData, setRouteData] = useState(null);

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
                setRouteData(data.routes)
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
            {routeData && routeData.map((route, index) => (
                <div className="row">
                    <div className="col">
                        <MapboxRenderLine route={route} />
                    </div>
                    <div className="col">
                        <div>City: {route.city}</div>
                        <div>Location: {route.location}</div>
                        <div>Time: {route.hours}:{route.minutes}</div>
                        <div>Difficulty: {route.difficulty}</div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default MyAccount;