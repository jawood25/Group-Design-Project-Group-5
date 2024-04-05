import { useState } from "react";
import React from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom'; // Import Link from React Router

const Friend = ({ username, isFriend }) => {
    const adder = useSelector((state) => state.userInfo.username)
    const [show, setShow] = useState(!isFriend);
    const onFollow = (friendUsername) => {
        setShow(false);
        fetch('/api/addingfriend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: adder, // Assuming you have a variable storing the current user's username
                friend_username: friendUsername,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.success) {
                alert('Friend added successfully!');
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    };    

    const onUnfollow = (friendUsername) => {
        setShow(true);
        fetch('/api/deletingfriend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: adder,
                friend_username: friendUsername,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.success) {
                alert('Friend deleted successfully!');
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    };   

    return (
        <div style={{ display: 'flex', alignItems: 'center', margin: 0, padding: "5px", background: "lightgrey", borderRadius: "35px", marginBottom: "25px", marginRight: "15px"}}>
            <Link to={`/profile/${username}`} style={{ margin: '0 auto', textDecoration: 'none', color: 'inherit' }}>
                <p>{username}</p>
            </Link>
            {show ? (
                <button className="btn btn-primary" style={{ margin: '0 auto' }} onClick={() => onFollow(username)}>Follow</button>
            ) : <button className="btn btn-primary" style={{ margin: '0 auto' }} onClick={() => onUnfollow(username)}>Unfollow</button>}
        </div>
    );
};

export default Friend;