import React, { useState } from 'react';
import Header from '../components/Header';
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux'
import { login, logout } from '../redux/loginStatus';


const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [login_failed, setLogin_failed] = useState(false)
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = {
            username: username,
            password: password
        };

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                console.log('Login successful');
                dispatch(login());
                navigate("/");
            } else {
                console.error('Login failed');
                setLogin_failed(true);
                dispatch(logout());
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className='Login'>
            <Header />

            <div class="container">
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <h2 class="text-center text-dark mt-5">Login</h2>
                        <div class="card my-5">

                            <form class="card-body cardbody-color p-lg-5" onSubmit={handleSubmit}>
                                <div class="mb-3">
                                    <input type="text" class="form-control" value={username} onChange={(e) => setUsername(e.target.value)} id="Username" aria-describedby="emailHelp"
                                        placeholder="User Name" />
                                </div>
                                <div class="mb-3">
                                    <input type="password" class="form-control" value={password} onChange={(e) => setPassword(e.target.value)} id="password" placeholder="password" />
                                </div>
                                <div class="text-center">
                                    { login_failed ? (
                                            <button type="submit" class="btn btn-color px-5 mb-2 w-100">Login</button>
                                        ) : (
                                            <button type="submit" class="btn btn-color px-5 mb-5 w-100">Login</button>
                                        )}
                                </div>
                                <div class="text-center">
                                    { login_failed ? (
                                            <div class="text-danger mb-3">Login Failed</div>
                                        ) : (<></>)}
                                </div>
                                <div id="emailHelp" class="form-text text-center mb-0 text-dark">
                                    Not Registered? <a href="/sign-up" class="text-blue fw-bold"> Create an Account</a>
                                </div>
                            </form>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;