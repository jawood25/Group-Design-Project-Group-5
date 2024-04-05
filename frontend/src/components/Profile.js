import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import MapboxRenderLine from  '../pages/MapboxRenderLine';
import '../style/myaccount.css'
import RouteSearch from '../components/RouteSearch';
import { useParams } from 'react-router-dom'; // Import useParams hook



const Profile = () => {
    const { friend_username } = useParams(); // Get the friend_username from URL params
    const username = useSelector((state) => state.userInfo.username)
    const [routeData, setRouteData] = useState(null);
    const [likedRouteData, setLikedRouteData] = useState(null);

    const likeRoute = (route_id) => {
        console.log("Route liked:", route_id);
        fetch("/api/savingroutes/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ route_id, username }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Route liked:", data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
    };

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
            data.routes = data.routes.filter(route => route.creator_username === friend_username)
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
                body: JSON.stringify({ username:friend_username }),
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
            data.routes = data.routes.filter(route => route.creator_username === friend_username)
            setRouteData(data.routes);
            if (data.routes.length === 0) {
                fetchUserRoutes();
            }
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    useEffect(() => {
        fetchUserRoutes();
        fetchUserLikedRoutes();
    }, [friend_username]);

    return (
        <div className='MyAccount'>
            <Header />
            <RouteSearch onSearch={handleSearch} />
            <h3>Username: {friend_username}</h3>
            <h2>Account Page</h2>
            <h4 id="mypaths">Paths</h4>
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
                            {route.comment && route.comment.length >= 1 && (
                            <div><b>Creator Comment:</b> {route.comment[0].body}</div>)}
                            {route.comment && route.comment.length >= 2 && (
                                //ignore the first comment as it is the creator comment
                            <div>
                                <b>Users Comment:</b> { route.comment.slice(1).map ((comment, index) => (
                                <div key={index}>
                                    {comment.author} : {comment.body}
                                </div>
                            ))}</div>)}
                        </div>                     
                        <button className="btn btn-primary" onClick={likeRoute(route.id)}>Like</button>
                    </div>
                ))}
            </div>
            <h4 className="mylikedpaths">Liked Paths</h4>
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
                            {route.comment && route.comment.length >= 1 && (
                            <div><b>Creator Comment:</b> {route.comment[0].body}</div>)}
                            {route.comment && route.comment.length >= 2 && (
                                //ignore the first comment as it is the creator comment
                            <div>
                                <b>Users Comment:</b> { route.comment.slice(1).map ((comment, index) => (
                                <div key={index}>
                                    {comment.author} : {comment.body}
                                </div>
                            ))}</div>)}
                        </div>
                        <button className="btn btn-primary"  onClick={likeRoute(route.id)}>Like</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Profile;