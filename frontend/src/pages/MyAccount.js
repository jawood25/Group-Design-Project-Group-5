// MyAccount.js
import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import MapboxRenderLine from './MapboxRenderLine';
import '../style/myaccount.css'
import RouteSearch from '../components/RouteSearch';
import Friend from '../components/Friend';


const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)
    const [routeData, setRouteData] = useState(null);
    const [likedRouteData, setLikedRouteData] = useState(null);
    const [friends, setFriends] = useState(null);


    const fetchUserRoutes = async () => {
        try {
            const response = await fetch('/api/searchroute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: '{}',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            data.routes = data.routes.filter(route => route.creator_username === username)
            setRouteData(data.routes);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const fetchUserLikedRoutes = async () => {
        try {
            const response = await fetch('/api/savedroutes', {
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
            setLikedRouteData(data.routes);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const fetchUserFriends = async () => {
        try {
            const response = await fetch('/api/usersfriends', {
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
            setFriends(data.friends);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };


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
            data.routes = data.routes.filter(route => route.creator_username === username)
            setRouteData(data.routes);
            if (data.routes.length === 0) {
                fetchUserRoutes();
            }
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const deleteRoute = async (routeId) => {
        try {
            const response = await fetch('/api/delete-route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username,  routeId}),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            await fetchUserRoutes()
        }
        catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

    const deleteLikedRoute = async (route_id) => {
        try {
            const response = await fetch('/api/unsavingroutes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username,  route_id}),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            await fetchUserLikedRoutes()
        }
        catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }
    
    useEffect(() => {
        fetchUserRoutes();
        fetchUserLikedRoutes();
        fetchUserFriends();
    }, []);

    return (
        <div className='MyAccount'>
            <Header />
            <h3>Username: {username}</h3>
            <h2>My Account Page</h2>
            <RouteSearch onSearch={handleSearch} />
            <h4>My Paths</h4>
            <div className="grid-container">
                {routeData && routeData.map((route, index) => (
                    <div className="grid-item" key={index}>
                        <MapboxRenderLine route={route} />
                        <div className="info">
                            <div><b>City:</b>  {route.city}</div>
                            <div><b>Location:</b>  {route.location}</div>
                            <div><b>Distance:</b>  {route.distance}km</div>
                            <div><b>Time:</b>  {route.hours}:{route.minutes}</div>
                            <div><b>Difficulty:</b>  {route.difficulty}</div>
                            <div><b>Mobility:</b>  {route.mobility}</div>
                            <div><b>Comment:</b>  {route.comment}</div>
                        </div>
                        <button onClick={() => deleteRoute(route.id)}>Delete</button>
                    </div>
                ))}
            </div>
            <h4>My Liked Paths</h4>
            <div className="grid-container">
                {likedRouteData && likedRouteData.map((route, index) => (
                    <div className="grid-item" key={index}>
                        <MapboxRenderLine route={route} />
                        <div className="info">
                            <div><b>City:</b>  {route.city}</div>
                            <div><b>Location:</b>  {route.location}</div>
                            <div><b>Distance:</b>  {route.distance}km</div>
                            <div><b>Time:</b>  {route.hours}:{route.minutes}</div>
                            <div><b>Difficulty:</b>  {route.difficulty}</div>
                            <div><b>Mobility:</b>  {route.mobility}</div>
                            <div><b>Comment:</b>  {route.comment}</div>
                        </div>
                        <button onClick={() => deleteLikedRoute(route.id)}>Delete</button>
                    </div>
                ))}
            </div>
            <div>
                {friends && friends.map((friend, index) => (
                    <Friend key={index} username={friend.username} isFriend={true}/>
                ))}
            </div>
        </div>
    );
};

export default MyAccount;