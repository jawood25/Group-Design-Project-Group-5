// Friend.js

import React from 'react';

const Friend = ({ username, onFollow }) => {
    return (
        <div style={{ display: 'flex', alignItems: 'center', margin: 0, padding:0 }}>
            <p style={{ marginRight: '10px' }}>{username}</p>
            <button style={{ marginLeft: 'auto' }} onClick={() => onFollow(username)}>Follow</button>
        </div>
    );
};

export default Friend;
