// Community.js

import React, { useState } from 'react';
import Friend from '../components/Friend';
import Header from '../components/Header';

const Community = () => {
    const [searchParams, setSearchParams] = useState({
        username: '',
        email: ''
    });
    const [searchResults, setSearchResults] = useState([]);

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
            setSearchResults(data); // Mettez à jour les résultats de la recherche
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
    };

    const handleFollow = (username) => {
        console.log(`Following user: ${username}`);
    };

    return (
        <div>
            <Header />
            <h2>Search Users</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" value={searchParams.username} onChange={handleChange} />
                <input type="text" name="email" placeholder="Email" value={searchParams.email} onChange={handleChange} />
                <button type="submit">Search</button>
            </form>
            <div>
                {searchResults.success && searchResults.users.length > 0 ? (
                    searchResults.users.map((user, index) => (
                        <Friend key={index} username={user.username} onFollow={handleFollow} />
                    ))
                ) : (
                    <p>No users found</p>
                )}
            </div>
        </div>
    );
};

export default Community;