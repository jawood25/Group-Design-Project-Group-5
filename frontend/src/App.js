import React, { useState, useEffect } from 'react';

function App() {
    // usestate for setting a javascript
    // object for storing and using data
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
        <div className="App">
            <h1>React and flask</h1>
            <p>{data.message}</p>
        </div>
    );
}
export default App;
