import React, { useState, useEffect } from 'react';
import Header from '../components/Header';

const Main = () => {
    const [data, setdata] = useState({
        message: "",
    });

    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("/api/data").then((res) =>
            res.json().then((data) => {
                // Setting a data from api
                setdata({
                    message: data.message
                });
            })
        );
    }, []);

    return (
        <div className='Main'>
            <Header />
            <p>{data.message}</p>
            <h2>Main Page</h2>
        </div>
    );
};

export default Main;