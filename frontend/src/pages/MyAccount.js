// MyAccount.js
import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect, useState } from 'react';
import MapboxRenderLine from './MapboxRenderLine';
import EditRoute from '../components/EditRoute';
import '../style/myaccount.css'
import RouteSearch from '../components/RouteSearch';
import Friend from '../components/Friend';
import { resetCoordinates } from '../redux/coordinates';
import { resetMapCenter } from '../redux/mapCenter';
import { useDispatch } from 'react-redux';


const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)
    const [routeData, setRouteData] = useState(null);
    const [likedRouteData, setLikedRouteData] = useState(null);
    const [friends, setFriends] = useState(null);
    const [friend_username, setSelectedFriend] = useState(null);
    const [editError, setEditError] = useState('');
    const [editSuccess, setEditSuccess] = useState('');
    const [comment, setComment] = useState('');

    const dispatch = useDispatch();
    const coordinates_edited = useSelector((state) => state.coordinates.coordinates)
    const mapCenter_edited = useSelector((state) => state.mapCenter.center)

    const shareRouteWithFriend = async (route_id) => {
        console.log(username, route_id, friend_username)
        try {
            const response = await fetch('/api/shareroute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, route_id, friend_username }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

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

    const commentRoad = async (route_id, body) => {
        try {
            const response = await fetch('/api/addingcomment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ route_id, body, author: username }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

    const deleteRoute = async (route) => {
        const routeInfo = {
            route_id: route.id,
            username: username,
            coordinates: route.coordinates,
            mapCenter: route.mapCenter,
            city: route.city,
            location: route.location,
            difficulty: route.difficulty,
            mobility: route.mobility,
        };
        try {
            const response = await fetch('/api/editroute', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(routeInfo),
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

    const editRoute = async (route) => {
        if (coordinates_edited.length > 1) {

            const routeData = {
                route_id: route.id,
                username: username,
                coordinates: coordinates_edited,
                mapCenter: mapCenter_edited,
                city: route.city,
                location: route.location,
                difficulty: route.difficulty,
                mobility: route.mobility,
            };
            try {
                const response = await fetch('/api/editroute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(routeData),
                });
                if (!response.ok) {
                    setEditError('Failed to edit the route. Please try again.');
                    throw new Error('Network response was not ok');
                }
                else {
                    const data = await response.json();
                    console.log(data)
                    dispatch(resetCoordinates());
                    dispatch(resetMapCenter());
                    await fetchUserRoutes()
                    setEditSuccess("Route successfully edited!")
                }
            }
            catch (error) {
                setEditError('Failed to edit the route. Please try again.');
                console.error('There was a problem with your fetch operation:', error);
            }
        }
    }

    const deleteLikedRoute = async (route_id) => {
        try {
            const response = await fetch('/api/unsavingroutes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, route_id }),
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
            <RouteSearch onSearch={handleSearch} />
            <h3>Username: {username}</h3>
            <h2>My Account Page</h2>
            <h4 id="mypaths">My Paths</h4>
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

                        <button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" onClick={() => {
                            setEditError('');
                            setEditSuccess('');
                        }}>
                            Edit Route
                        </button>

                        <div className="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered modal-xl">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">Edit your route</h5>
                                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div className="modal-body">
                                        <EditRoute route={route} />
                                    </div>
                                    <div className="modal-footer">
                                        {editError && <div className="alert alert-danger" role="alert">{editError}</div>}
                                        {editSuccess && <div className="alert alert-success" role="alert">{editSuccess}</div>}
                                        <button type="button" className="btn btn-primary" onClick={() => editRoute(route)}>Save changes</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <button className="btn btn-primary" onClick={() => deleteRoute(route)}>Delete Route</button>
                        <input type="text" placeholder="Comment" onChange={(e)=> setComment(e.target.value)}/>
                        <button onClick={() => commentRoad(route.id, comment)}>Comment</button>
                        <select className="friendSelect" onChange={(e) => setSelectedFriend(e.target.value)}>
                            <option value="">Select Friend</option>
                            {friends && friends.map((friend, index) => (
                                <option key={index} value={friend.username}>{friend.username}</option>
                            ))}
                        </select>
                        <button className="sharebtn" onClick={() => shareRouteWithFriend(route.id)}>Share</button>
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
                        <button onClick={() => deleteLikedRoute(route.id)}>Delete</button>
                        <input type="text" placeholder="Comment" onChange={(e)=> setComment(e.target.value)}/>
                        <button onClick={() => commentRoad(route.id, comment)}>Comment</button>
                        <select onChange={(e) => setSelectedFriend(e.target.value)}>
                            <option value="">Select Friend</option>
                            {friends && friends.map((friend, index) => (
                                <option key={index} value={friend.username}>{friend.username}</option>
                            ))}
                        </select>
                        <button onClick={() => shareRouteWithFriend(route.id)}>Share</button>
                    </div>
                ))}
            </div>
            <div>
                {friends && friends.map((friend, index) => (
                    <Friend key={index} username={friend.username} isFriend={true} />
                ))}
            </div>
        </div>
    );
};

export default MyAccount;