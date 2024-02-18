import Header from '../components/Header';
import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { useSelector } from 'react-redux';


const Upload = () => {
    const isLoggedIn = useSelector((state) => state.loginStatus.isLoggedIn);
    const [googleMyMapURL, setGoogleMyMapURL] = useState('');
    const [city, setCity] = useState('');
    const [location, setLocation] = useState('');
    const [hours, setHours] = useState('');
    const [minutes, setMinutes] = useState('');
    const [difficulty, setDifficulty] = useState('')
    const [desc, setDesc] = useState('')
    const username = useSelector((state) => state.userInfo.username)

    const navigate = useNavigate();

    const isValidGoogleMapURL = (url) => {
        const pattern = /^https:\/\/www\.google\.com\/maps\/d\/u\/0\/edit\?mid=.+&usp=sharing$/;
        return pattern.test(url);
    };


    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!isValidGoogleMapURL(googleMyMapURL)) {
            alert('Invalid Google Map URL. Please enter a valid URL.');
            return;
        }
        
        const kmlURL = googleMyMapURL.replace('/edit?', '/kml?').replace('usp=sharing', 'forcekml=1');

        const formData = {
            username: username,
            kmlURL: kmlURL,
            city: city,
            location: location,
            hours: parseInt(hours),
            minutes: parseInt(minutes),
            difficulty: difficulty,
            desc: desc
        };

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                console.log('Upload successful');
                navigate("/my-account");
            } else {
                console.error('Upload failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    return (
        <div className='Upload'>
            <Header />
            {isLoggedIn ? (
                <div className="container upload-route">
                    <div className="row">
                        <div className="col-md-3">
                            <div className="upload-route-info">
                                <h2>Share Your Running Route</h2>
                                <h4>Join Our Running Community !</h4>
                            </div>
                        </div>
                        <div className="col-md-9">
                            <form className="upload-route-form" onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <label className="control-label col-sm-2" htmlFor="kml" style={{ whiteSpace: 'nowrap' }}>Your Route URL:</label>
                                    <div className="col-sm-10">
                                        <input type="text" className="form-control" value={googleMyMapURL} onChange={(e) => setGoogleMyMapURL(e.target.value)} id="kml" placeholder="Enter your route URL (from Google My Map)" />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="control-label col-sm-2" htmlFor="city">City:</label>
                                    <div className="col-sm-10">
                                        <input type="text" className="form-control" value={city} onChange={(e) => setCity(e.target.value)} id="city" placeholder="Enter the name of the city you ran in" />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="control-label col-sm-2" htmlFor="location">Location:</label>
                                    <div className="col-sm-10">
                                        <input type="text" className="form-control" id="location" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Enter the location you ran in (e.g. Trinity College Dublin)" />
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="control-label col-sm-2">Time:</label>
                                    <div className="col-sm-10">
                                        <div className="row">
                                            <div className="col-sm-2">
                                                <input type="number" className="form-control" value={hours} onChange={(e) => setHours(e.target.value)} id="hours" />
                                            </div>
                                            <label className="col-sm-1 control-label d-flex align-items-center" htmlFor="hours">hours</label>
                                            <div className="col-sm-2">
                                                <input type="number" className="form-control" value={minutes} onChange={(e) => setMinutes(e.target.value)} id="minutes" />
                                            </div>
                                            <label className="col-sm-1 control-label d-flex align-items-center" htmlFor="minutes">minutes</label>
                                        </div>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="control-label col-sm-2">Difficulty:</label>
                                    <div className="col-sm-10">
                                        <div className="form-check form-check-inline">
                                            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="Easy" onChange={(e) => setDifficulty(e.target.value)} />
                                            <label className="form-check-label" htmlFor="inlineRadio1">Easy</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="Normal" onChange={(e) => setDifficulty(e.target.value)} />
                                            <label className="form-check-label" htmlFor="inlineRadio2">Normal</label>
                                        </div>
                                        <div className="form-check form-check-inline">
                                            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="Hard" onChange={(e) => setDifficulty(e.target.value)} />
                                            <label className="form-check-label" htmlFor="inlineRadio3">Hard</label>
                                        </div>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <label className="control-label col-sm-2" htmlFor="description">Description:</label>
                                    <div className="col-sm-10">
                                        <textarea className="form-control" rows="5" value={desc} onChange={(e) => setDesc(e.target.value)} id="description"></textarea>
                                    </div>
                                </div>
                                <div className="form-group">
                                    <div className="col-sm-offset-2 col-sm-10 text-center mt-5">
                                        <button type="submit" className="btn btn-default">Share</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            ) : (
                <div>
                    <h2>You need to login to your account first.</h2>
                </div>
            )}
        </div>
    );
};

export default Upload;