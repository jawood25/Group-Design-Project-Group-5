import React from 'react';
import { useSelector } from 'react-redux';


const Comment = ({ author, body, owner, onDelete }) => {
    const username = useSelector((state) => state.userInfo.username)
    return (
        <div className="comment">
            <p><strong>{author}</strong>: {body}</p>
            {(author === username || username === owner) && <button onClick={onDelete}>X</button>}      
        </div>
    );
};

export default Comment;