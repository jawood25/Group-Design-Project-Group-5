import React from 'react';
import Header from '../components/Header';

const SignUp = () => {
    return (
        <div className="SignUp">
            <Header />
            <div class="container">
                <div class="row">
                    <div class="col-md-6 offset-md-3">
                        <h2 class="text-center text-dark mt-5">Sign Up</h2>
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
                                    <button type="submit" className="btn btn-color px-5 mb-5 w-100">Sign up</button>
                                </div>
                                <div id="emailHelp" class="form-text text-center mb-0 text-dark">
                                    Already Registered? <a href="/login" class="text-blue fw-bold"> Login</a>
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