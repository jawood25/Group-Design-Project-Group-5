import React from 'react';
import Header from '../components/Header';


const Login = () => {
    return (
        <div className='Login'>
            <Header />

            <div class="container">
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <h2 class="text-center text-dark mt-5">Login</h2>
                        <div class="card my-5">

                            <form class="card-body cardbody-color p-lg-5">
                                <div class="mb-3">
                                    <input type="text" class="form-control" id="Username" aria-describedby="emailHelp"
                                        placeholder="User Name" />
                                </div>
                                <div class="mb-3">
                                    <input type="password" class="form-control" id="password" placeholder="password" />
                                </div>
                                <div class="text-center">
                                    <button type="submit" class="btn btn-color px-5 mb-5 w-100">Login</button>
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