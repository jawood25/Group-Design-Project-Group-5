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
import Comment from '../components/Comment';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';


const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)
    const [routeData, setRouteData] = useState(null);
    const [likedRouteData, setLikedRouteData] = useState(null);
    const [friends, setFriends] = useState(null);
    const [friend_username, setSelectedFriend] = useState(null);
    const [groupList, setGroupList] = useState(null);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [editError, setEditError] = useState('');
    const [editSuccess, setEditSuccess] = useState('');
    const [comment, setComment] = useState('');
    const [groups, setGroups] = useState(null);
    const [groupsIManage, setGroupsIManage] = useState(null);

    const [meetingPlace, setMeetingPlace] = useState('');
    const [meetingTime, setMeetingTime] = useState({ hour: '00', minute: '00' });
    const [generalInfo, setGeneralInfo] = useState('');
    const [selectedDate, setSelectedDate] = useState(new Date());
    const hours = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));
    const minutes = Array.from({ length: 60 }, (_, i) => i.toString().padStart(2, '0'));
    const [eventRoute, setEventRoute] = useState(null);

    const [selectedOption, setSelectedOption] = useState('Friend');



    const dispatch = useDispatch();
    const coordinates_edited = useSelector((state) => state.coordinates.coordinates)
    const mapCenter_edited = useSelector((state) => state.mapCenter.center)

    const deleteComment = async (comment_id) => {
        try {
            const response = await fetch('/api/deletecomment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ comment_id }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            await fetchUserRoutes();
            await fetchUserLikedRoutes();
        }
        catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

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

    const shareRouteWithGroup = async (route_id) => {
        const group = groupList.filter(group => group.name === selectedGroup);
        const members = group[0].members
        console.log(members)
        try {
            const response = await fetch('/api/shareroute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, route_id, members }),
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

    const fetchGroups = async () => {
        try {
            const response = await fetch('/api/getgroup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data.groups)

            setGroupsIManage(data.groups.filter(group => group.manager === username));
            setGroups(data.groups.filter(group => group.members.find(member => member.username === username)));
            const combinedGroups = [...data.groups.filter(group => group.manager === username), ...data.groups.filter(group => group.members.find(member => member.username === username))];
            setGroupList(combinedGroups)
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
            await fetchUserRoutes();
            await fetchUserLikedRoutes();
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

    const deleteGroup = async (group_name, username) => {
        try {
            const response = await fetch('/api/deletegroup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ groupname: group_name, manager: username }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            await fetchGroups();
        }
        catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

    const leaveGroup = async (group_name, username) => {
        try {
            const response = await fetch('/api/leavinggroup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ groupname: group_name, username: username }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            await fetchGroups();
        }
        catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

    const uploadEvent = async (e) => {
        e.preventDefault();

        const datePart = selectedDate.toISOString().split('T')[0];
        const timePart = `${meetingTime.hour}:${meetingTime.minute}:00`;

        const eventData = {
            username,
            routeId: eventRoute.id,
            meetingPlace,
            meetingTime: `${datePart}T${timePart}`,
            generalInfo,
            friends
        };

        try {
            const response = await fetch('/api/sharedevent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    useEffect(() => {
        fetchUserRoutes();
        fetchUserLikedRoutes();
        fetchUserFriends();
        fetchGroups();
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
                            <div><b>Time:</b>  {
                                (() => {
                                    const totalMinutes = route.minutes;
                                    const hours = Math.floor(totalMinutes / 60);
                                    const minutes = totalMinutes % 60;
                                    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
                                })()
                            }</div>
                            <div><b>Difficulty:</b>  {route.difficulty}</div>
                            <div><b>Mobility:</b>  {route.mobility}</div>
                            {route.comment && route.comment.length >= 1 && (
                                <div><b>Creator Comment:</b> {route.comment[0].body}</div>)}
                            {route.comment && route.comment.length >= 2 && (
                                //ignore the first comment as it is the creator comment
                                <div>
                                    <b>Users Comment:</b> {route.comment.slice(1).map((comment, index) => (
                                        <div key={index}>
                                            {console.log(comment)}
                                            <Comment
                                                author={comment.author}
                                                body={comment.body}
                                                owner={username}
                                                onDelete={() => deleteComment(comment.id)}
                                            />
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

                        <button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#eventModal" onClick={() => setEventRoute(route)}>
                            Create Event
                        </button>

                        <div className="modal fade" id="eventModal" tabIndex="-1" aria-labelledby="eventModalLabel" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered modal-xl">
                                <div className="modal-content">
                                    <form onSubmit={uploadEvent}>
                                        <div className="modal-header">
                                            <h5 className="modal-title" id="eventModalLabel">Create an exercise event</h5>
                                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div className="modal-body p-5">
                                            <div className="mb-4">
                                                <div className="row align-items-center">
                                                    <div className="col-auto">
                                                        <label htmlFor="meetingPlace" className="form-label mb-0" style={{ fontSize: "20px" }}>Meeting Place :</label>
                                                    </div>
                                                    <div className="col">
                                                        <input type="text" className="form-control" id="meetingPlace" value={meetingPlace} onChange={(e) => setMeetingPlace(e.target.value)} required />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="mb-3">
                                                <div className="row align-items-center">
                                                    <div className="col-auto">
                                                        <label htmlFor="meetingDate" className="form-label mb-0" style={{ fontSize: "20px" }}>Meeting Date :</label>
                                                    </div>
                                                    <div className="col-auto">
                                                        <DatePicker
                                                            selected={selectedDate}
                                                            onChange={(date) => setSelectedDate(date)}
                                                            dateFormat="dd/MM/yyyy"
                                                            className="form-control"
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="mb-3">
                                                <div className="row align-items-center">
                                                    <div className="col-auto">
                                                        <label htmlFor="meetingTimeHour" className="form-label mb-0" style={{ fontSize: "20px" }}>Meeting Time :</label>
                                                    </div>
                                                    <div className="col-auto">
                                                        <select className="form-select" id="meetingTimeHour" value={meetingTime.hour} onChange={(e) => setMeetingTime({ ...meetingTime, hour: e.target.value })} required>
                                                            {hours.map(hour => <option key={hour} value={hour}>{hour}</option>)}
                                                        </select>
                                                    </div>
                                                    <div className="col-auto">
                                                        <span style={{ fontSize: "20px", fontWeight: "bold" }}>:</span>
                                                    </div>
                                                    <div className="col-auto">
                                                        <select className="form-select" id="meetingTimeMinute" value={meetingTime.minute} onChange={(e) => setMeetingTime({ ...meetingTime, minute: e.target.value })} required>
                                                            {minutes.map(minute => <option key={minute} value={minute}>{minute}</option>)}
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="mb-3">
                                                <label htmlFor="generalInfo" className="form-label" style={{ fontSize: "20px" }}>General Information</label>
                                                <textarea className="form-control" id="generalInfo" value={generalInfo} onChange={(e) => setGeneralInfo(e.target.value)} required />
                                            </div>
                                        </div>
                                        <div className="modal-footer">
                                            <button type="submit" className="btn btn-primary btn-lg">Share!</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>

                        <button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#shareModal">
                            Share
                        </button>

                        <div className="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered modal-xl">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">Share your route</h5>
                                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div className="modal-body">
                                        <div className="container mt-3">
                                            <div className="mb-3">
                                                <div className="form-check form-check-inline">
                                                    <input className="form-check-input" type="radio" name="inlineRadioOptions" id="radio1" value="Friend" onChange={(e) => setSelectedOption(e.target.value)} />
                                                    <label className="form-check-label" htmlFor="radio1">Friend</label>
                                                </div>
                                                <div className="form-check form-check-inline">
                                                    <input className="form-check-input" type="radio" name="inlineRadioOptions" id="radio2" value="Group" onChange={(e) => setSelectedOption(e.target.value)} />
                                                    <label className="form-check-label" htmlFor="radio2">Group</label>
                                                </div>
                                            </div>

                                            {selectedOption === 'Friend' ? (
                                                <div className='d-flex justify-content-center'>
                                                    <select class="form-select" onChange={(e) => setSelectedFriend(e.target.value)}>
                                                        <option value="" selected>Select Friend</option>
                                                        {friends && friends.map((friend, index) => (
                                                            <option key={index} value={friend.username}>{friend.username}</option>
                                                        ))}
                                                    </select>
                                                </div>
                                            ) : (
                                                <div className='d-flex justify-content-center'>
                                                    <select class="form-select" onChange={(e) => setSelectedGroup(e.target.value)}>
                                                        <option value="" selected>Select Group</option>
                                                        {groupList && groupList.map((group, index) => (
                                                            <option key={index} value={group.name}>{group.name}</option>
                                                        ))}
                                                    </select>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <div className="modal-footer">
                                        {selectedOption === 'Friend' ? (
                                            <div>
                                                <button className="sharebtn" onClick={() => shareRouteWithFriend(route.id)}>Share</button>
                                            </div>
                                        ) : (
                                            <div>
                                                <button className="sharebtn" onClick={() => shareRouteWithGroup(route.id)}>Share</button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <input type="text" className="commentinput" placeholder="Comment..." onChange={(e) => setComment(e.target.value)} />
                        <button className="commentbutton" onClick={() => commentRoad(route.id, comment)}>Publish Comment</button>
                    </div>
                ))}
            </div>
            <h4 className="mylikedpaths">My Liked Paths</h4>
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
                                    <b>Users Comment:</b> {route.comment.slice(1).map((comment, index) => (
                                        <div key={index}>
                                            <Comment
                                                author={comment.author}
                                                body={comment.body}
                                                owner={route.creator_username}
                                                onDelete={() => deleteComment(comment.id)}
                                            />
                                        </div>
                                    ))}</div>)}
                        </div>
                        <button className="btn btn-primary" onClick={() => deleteLikedRoute(route.id)}>Unlike</button>
                        <button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#shareModal">Share</button>

                        <div className="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered modal-xl">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">Share your route</h5>
                                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div className="modal-body">
                                        <div className="container mt-3">
                                            <div className="mb-3">
                                                <div className="form-check form-check-inline">
                                                    <input className="form-check-input" type="radio" name="inlineRadioOptions" id="radio1" value="Friend" onChange={(e) => setSelectedOption(e.target.value)} />
                                                    <label className="form-check-label" htmlFor="radio1">Friend</label>
                                                </div>
                                                <div className="form-check form-check-inline">
                                                    <input className="form-check-input" type="radio" name="inlineRadioOptions" id="radio2" value="Group" onChange={(e) => setSelectedOption(e.target.value)} />
                                                    <label className="form-check-label" htmlFor="radio2">Group</label>
                                                </div>
                                            </div>

                                            {selectedOption === 'Friend' ? (
                                                <div className='d-flex justify-content-center'>
                                                    <select class="form-select" onChange={(e) => setSelectedFriend(e.target.value)}>
                                                        <option value="" selected>Select Friend</option>
                                                        {friends && friends.map((friend, index) => (
                                                            <option key={index} value={friend.username}>{friend.username}</option>
                                                        ))}
                                                    </select>
                                                </div>
                                            ) : (
                                                <div className='d-flex justify-content-center'>
                                                    <select class="form-select" onChange={(e) => setSelectedGroup(e.target.value)}>
                                                        <option value="" selected>Select Group</option>
                                                        {groupList && groupList.map((group, index) => (
                                                            <option key={index} value={group.name}>{group.name}</option>
                                                        ))}
                                                    </select>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <div className="modal-footer">
                                        {selectedOption === 'Friend' ? (
                                            <div>
                                                <button className="sharebtn" onClick={() => shareRouteWithFriend(route.id)}>Share</button>
                                            </div>
                                        ) : (
                                            <div>
                                                <button className="sharebtn" onClick={() => shareRouteWithGroup(route.id)}>Share</button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <input className="commentinput" type="text" placeholder="Comment" onChange={(e) => setComment(e.target.value)} />
                        <button className="commentbutton" onClick={() => commentRoad(route.id, comment)}>Publish Comment</button>
                        
                        
                    </div>
                ))}
            </div>
            <h2 id="groupsh2">The Groups</h2>
            <h4>My Groups</h4>
            <div id="groupsdiv">
                {groupsIManage && groupsIManage.map((group, index) => (
                    <div className="group" key={index}>
                        <h4>{group.name}</h4>
                        <h6>Manager: {group.manager}</h6>
                        <h6>Members:</h6>
                        <ul>
                            {group.members.map((member, idx) => (
                                <div className="groupsubdiv">
                                    <li key={idx}>{member.username}</li>
                                    <button className="btn btn-primary btn-groups" onClick={() => leaveGroup(group.name, member.username)}>Kick</button>
                                </div>
                            ))}
                        </ul>
                        <button className="btn btn-primary btn-groups" onClick={() => deleteGroup(group.name, username)}>Delete</button>
                    </div>
                ))}
            </div>
            <h4>Groups I am in</h4>
            <div id="groupsdiv">
                {groups && groups.map((group, index) => (
                    <div className="group" key={index}>
                        <h4>{group.name}</h4>
                        <h6>Manager : {group.manager}</h6>
                        <h6>Members:</h6>
                        <ul>
                            {group.members.map((member, idx) => (
                                <div className="groupsubdiv">
                                    <li key={idx}>{member.username}</li>
                                </div>
                            ))}
                        </ul>
                        <button className="btn btn-primary btn-groups" onClick={() => leaveGroup(group.name, username)}>Leave Group</button>
                    </div>
                ))}
            </div>
            <h4>My Friends</h4>
            <div id="friendsdiv">
                {friends && friends.map((friend, index) => (
                    <Friend className="acctfriend" key={index} username={friend.username} isFriend={true} />
                ))}
            </div>
        </div>
    );
};

export default MyAccount;