import React, { useState } from 'react';
import Header from '../components/Header';
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux'
import { login, logout } from '../redux/loginStatus';
import { Link } from 'react-router-dom';


const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [login_failed, setLogin_failed] = useState(false)
    const [Username_does_not_exist, setUsername_does_not_exist] = useState(false)
    const [Incorrect_password, setIncorrect_password] = useState(false)
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
                const responseData = await response.json();
                console.log(responseData)
                dispatch(login());
                navigate("/");
            }
            else if (response.status == 400){
                console.log('Incorrect password')
                setIncorrect_password(true);
                dispatch(logout());
            }
            else if (response.status == 401) {
                console.log('Username does not exist')
                setUsername_does_not_exist(true);
                dispatch(logout());
            } 
            else {
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

            <div className="container">
                <div className="row">
                    <div className="col-md-6 offset-md-3">
                        <h2 className="text-center text-dark mt-5">Login</h2>
                        <div className="card my-5">

                            <form className="card-body cardbody-color p-lg-5" onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} id="Username" aria-describedby="emailHelp"
                                        placeholder="User Name" />
                                </div>
                                <div className="mb-3">
                                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} id="password" placeholder="password" />
                                </div>
                                <div className="text-center">
                                    { login_failed ? (
                                            <button type="submit" className="btn btn-color px-5 mb-2 w-100">Login</button>
                                        ) : (
                                            <button type="submit" className="btn btn-color px-5 mb-5 w-100">Login</button>
                                        )}
                                </div>
                                <div className="text-center">
                                    { login_failed ? (
                                            <div className="text-danger mb-3">Login Failed</div>
                                        ) : (<></>)}
                                </div>
                                <div className="text-center">
                                    { Username_does_not_exist ? (
                                            <div className="text-danger mb-3">Username does not exist</div>
                                        ) : (<></>)}
                                </div>
                                <div className="text-center">
                                    { Incorrect_password ? (
                                            <div className="text-danger mb-3">Incorrect password</div>
                                        ) : (<></>)}
                                </div>
                                <div id="emailHelp" className="form-text text-center mb-0 text-dark">
                                    Not Registered? <Link to="/sign-up" className="text-blue fw-bold"> Create an Account</Link>
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