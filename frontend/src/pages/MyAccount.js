import Header from '../components/Header';
import { useSelector } from 'react-redux';
import React, { useEffect } from 'react';

const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)

    useEffect(() => {
    }, []);

    return (
        <div className='MyAccount'>
            <Header />
            <h2>My Account Page</h2>
            <h3>Username: {username}</h3>
        </div>
    );
};

export default MyAccount;