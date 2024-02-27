import React, { useState } from 'react';
import Header from '../components/Header';
import { Link } from 'react-router-dom';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [Username_already_exists, setUsername_already_exists] = useState(false)


    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = {
            username: username,
            password: password
        };

        try {
            const response = await fetch('/api/sign-up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                console.log('Sign up successful');
            }
            
            else if (response.status == 405){
                console.log('Username already exists')
                setUsername_already_exists(true);
            }
            else {
                console.error('Sign up failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="SignUp">
            <Header />
            <div className="container">
                <div className="row">
                    <div className="col-md-6 offset-md-3">
                        <h2 className="text-center text-dark mt-5">Sign Up</h2>
                        <div className="card my-5">
                            <form className="card-body cardbody-color p-lg-5" onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} id="Username" aria-describedby="emailHelp" placeholder="User Name" />
                                </div>
                                <div className="mb-3">
                                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} id="password" placeholder="password" />
                                </div>
                                <div className="text-center">
                                    <button type="submit" className="btn btn-color px-5 mb-5 w-100">Sign up</button>
                                </div>
                                <div className="text-center">
                                    { Username_already_exists ? (
                                            <div className="text-danger mb-3">Username already exists</div>
                                        ) : (<></>)}
                                </div>
                                <div id="emailHelp" className="form-text text-center mb-0 text-dark">
                                    Already Registered? <Link to="/login" className="text-blue fw-bold"> Login</Link>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SignUp;