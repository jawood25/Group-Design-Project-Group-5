import Header from '../components/Header';
import { useSelector } from 'react-redux';
import { useEffect, useState } from 'react';

const MyAccount = () => {
    const [userData, setUserData] = useState(null); // 受け取ったユーザーデータを保存するstate
    const username = useSelector((state) => state.userInfo.username)

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch('/api/userroutes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }),
                });
                if (!response.ok) {
                    throw new Error('fetch api failed');
                }
                const data = await response.json();
                setUserData(data);
            } catch (error) {
                console.error('fetch api failed 2', error);
            }
        };

        fetchUserData(); 
    }, []);

    return (
        <div className='MyAccount'>
            <Header />
            <h2>My Account Page</h2>
            <h3>Username: {username}</h3>
            <h4>{userData}</h4>
        </div>
    );
};

export default MyAccount;