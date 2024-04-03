import React, { useState, useEffect } from 'react';
import Friend from '../components/Friend';
import Header from '../components/Header';
import { useSelector } from 'react-redux';
import '../style/community.css';
import MapboxRenderLine from './MapboxRenderLine';

const Community = () => {
    const username = useSelector((state) => state.userInfo.username);
    const [friends, setFriends] = useState(null);
    const [sharedRoutes, setSharedRoutes] = useState(null);
    const [searchParams, setSearchParams] = useState({
        username: '',
        email: ''
    });
    const [searchResults, setSearchResults] = useState([]);
    const [showSearch, setShowSearch] = useState(false); // State to control the visibility of search form
    const [selectedFriends, setSelectedFriends] = useState([]);
    const [groupName, setGroupName] = useState('');

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
            setFriends(data.friends);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const likeRoute = (route_id) => {
        const checkbox = document.getElementById("liketoggle");
        checkbox.checked = !checkbox.checked;
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

    const fetchUserSharedRoutes = async () => {
        try {
            const response = await fetch('/api/usersharedroutes', {
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
            setSharedRoutes(data.routes.sort((a, b) => (a.shared_by > b.shared_by) ? 1 : -1));
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const handleChange = (e) => {
        setSearchParams({
            ...searchParams,
            [e.target.name]: e.target.value
        });
    };

    const handleUserSearch = async (searchParams) => {
        try {
            const response = await fetch('/api/searchuser', {
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
            data.users = data.users.filter(user => user.username !== username);
            data.users = data.users.filter(user => friends.every(friend => friend.username !== user.username));
            setSearchResults(data);
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const filteredParams = {};
        Object.keys(searchParams).forEach(key => {
            if (searchParams[key] !== '') {
                filteredParams[key] = searchParams[key];
            }
        });
        handleUserSearch(filteredParams);
        setShowSearch(true); // Show search results after form submission
    };
    
    useEffect(() => {
        fetchUserFriends();
        fetchUserSharedRoutes();
    }, []);

    const toggleSearch = () => {
        setShowSearch(!showSearch);
    };

    const handleFriendSelect = (friend) => {
        // Check if the friend is already selected, if not add, otherwise remove
        if (selectedFriends.includes(friend.username)) {
            setSelectedFriends(selectedFriends.filter(username => username !== friend.username));
        } else {
            setSelectedFriends([...selectedFriends, friend.username]);
        }
    };    

    const handleCreateGroup = (e) => {
        e.preventDefault();
        console.log("Group Name:", groupName);
        console.log("Selected Friends:", selectedFriends);
        setSelectedFriends([]);
        setGroupName('');
        fetch("/api/creategroup/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: groupName, manager:username, members:selectedFriends }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            }
            )
            .then(data => {
                console.log("Group created:", data);
                alert('Group created successfully!');
            }
            )
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            }
            );
    };
    
    return (
        <div className='Community'>
            <Header />
            <h2 id="communityHeading" onClick={toggleSearch}>Search New Friends🔎</h2>
            {showSearch && (
                <div>
                    <form id="userSearchForm" onSubmit={handleSubmit}>
                        <input type="text" name="username" placeholder="Username" value={searchParams.username} onChange={handleChange} />
                        <input type="text" name="email" placeholder="Email" value={searchParams.email} onChange={handleChange} />
                        <button type="submit" id="submitbutton">Search</button>
                    </form>
                    <div className='resultDiv'>
                        {searchResults.success && searchResults.users.length > 0 ? (
                            searchResults.users.map((user, index) => {
                                return (
                                    <Friend key={index} username={user.username} email={user.email} isFriend={false} />
                                );
                            })
                        ) : (
                            <p>No users found</p>
                        )}
                    </div>
                </div>
            )}
            <h4 id="mypaths">Your Friends Shared you some Paths !</h4>
            <div className="grid-container">
                {sharedRoutes && sharedRoutes.map((object, index) => (
                    <div key={index}>
                        <div className="nameshared">{object.shared_by} shared to you:</div>
                        <div className="grid-item">
                            <MapboxRenderLine route={object} />
                            <div className="info">
                                <div><b>City:</b>  {object.city}</div>
                                <div><b>Location:</b>  {object.location}</div>
                                <div><b>Distance:</b>  {object.distance}km</div>
                                <div><b>Time:</b>  {object.hours}:{object.minutes}</div>
                                <div><b>Difficulty:</b>  {object.difficulty}</div>
                                <div><b>Mobility:</b>  {object.mobility}</div>
                                {object.comment && object.comment.length >= 1 && (
                                    <div><b>Creator Comment:</b> {object.comment[0].body}</div>)}
                                <div>
                                    <input type="checkbox" id="liketoggle" className="liketoggle"></input>
                                    <button className="like-button"  onClick={() => likeRoute(object.id)}></button>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            {friends && friends.length > 0 && (
            <div id="groupdiv">
                <h2>Create a Group</h2>
                <form onSubmit={handleCreateGroup}>
                    <input type="text" id="groupnameinput" placeholder="Group Name" value={groupName} onChange={(e) => setGroupName(e.target.value)} />
                    <ul>
                        {friends.map((friend, index) => (
                            <li id="friendlist" key={index}>
                                <label className="friendlabel">
                                    <input type="checkbox" class="friendcheckbox" onChange={() => handleFriendSelect(friend)} />
                                    {friend.username}
                                </label>
                            </li>
                        ))}
                    </ul>
                    <button type="submit" id="groupbutton">Create Group</button>
                </form>
            </div>
            )}
        </div>
    );
};

export default Community;