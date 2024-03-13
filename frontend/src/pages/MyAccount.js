import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import MapboxRenderLine from './MapboxRenderLine';
import '../style/myaccount.css'

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
            <h3>Username: {username}</h3>
            <h2>My Account Page</h2>
            <div className="grid-container">
                {routeData && routeData.map((route, index) => (
                    <div className="grid-item">
                        <MapboxRenderLine route={route} />
                        <div className="info">
                            <div><b>City:</b>  {route.city}</div>
                            <div><b>Location:</b>  {route.location}</div>
                            <div><b>Time:</b>  {route.hours}:{route.minutes}</div>
                            <div><b>Difficulty:</b>  {route.difficulty}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MyAccount;