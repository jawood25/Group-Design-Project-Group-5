import Header from '../components/Header';
import Map from "../components/Map"
import { useSelector } from 'react-redux';
import { useEffect } from 'react';

const MyAccount = () => {
    const username = useSelector((state) => state.userInfo.username)

    useEffect(() => {
    }, []);

    return (
        <div className='MyAccount'>
            <Header />
            <h2>My Account Page</h2>
            <h3>Username: {username}</h3>
            <Map />
        </div>
    );
};

export default MyAccount;