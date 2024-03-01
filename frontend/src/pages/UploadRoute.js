import Header from '../components/Header';
import MapboxDrawLine from './MapBoxDrawLine';
import { useSelector } from 'react-redux';
import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from 'react';
import '../style/upload.css'

const UploadRoute = () => {
    const [city, setCity] = useState('');
    const [location, setLocation] = useState('');
    const [geoData, setGeoData] = useState(null);
    const [mapFlag, setMapFlag] = useState(false)
    const [hours, setHours] = useState('');
    const [minutes, setMinutes] = useState('');
    const [difficulty, setDifficulty] = useState('')
    const [comment, setComment] = useState('')

    const username = useSelector((state) => state.userInfo.username)
    const coordinates = useSelector((state) => state.coordinates.coordinates)
    const navigate = useNavigate();

    const getCoordinates = async (e) => {
        e.preventDefault();
        let geoCodeAPIURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=location+city&language=en&key='
        geoCodeAPIURL = geoCodeAPIURL.replace("location", location).replace("city", city)
        try {
            const response = await fetch(geoCodeAPIURL);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setGeoData(data.results[0]);
            setMapFlag(true)
        } catch (error) {
            console.error('There was a problem with your fetch operation:', error);
        }
    }

    const upload = async (e) => {
        e.preventDefault();
        const formData = {
            username: username,
            coordinates: coordinates,
            city: city,
            location: location,
            hours: parseInt(hours),
            minutes: parseInt(minutes),
            difficulty: difficulty,
            desc: comment
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
        console.log(coordinates)
    }

    useEffect(() => {
    }, []);

    return (
        <div className='UploadRoute'>
            <Header />
            <div className="card">
                <div className="card-body">
                    <h5 className="card-title">Upload Your Route</h5>
                    <div className="accordion" id="accordionPanelsStayOpenExample">
                        <div className="accordion-item">
                            <h2 className="accordion-header">
                                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                                    Search your exercise location
                                </button>
                            </h2>
                            <div id="panelsStayOpen-collapseOne" className="accordion-collapse collapse show">
                                <div className="accordion-body">
                                    <div className="container text-center">
                                        <form onSubmit={getCoordinates}>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col">
                                                        <label className="control-label" htmlFor="city">City:</label>
                                                        <input type="text" className="form-control" value={city} onChange={(e) => setCity(e.target.value)} id="city" placeholder="Enter the name of the city you ran in" />
                                                    </div>
                                                    <div className="col">
                                                        <label className="control-label" htmlFor="location">Location:</label>
                                                        <input type="text" className="form-control" id="location" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Enter the location you ran in (e.g. Trinity College Dublin)" />
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="form-group">
                                                <div className="row">
                                                    <div className="col">
                                                        <button type="submit" className="btn btn-color btn-default">Get Map</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="accordion-item">
                            <h2 className="accordion-header">
                                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseTwo" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                                    Create Your Route
                                </button>
                            </h2>
                            <div id="panelsStayOpen-collapseTwo" className="accordion-collapse collapse">
                                <div className="accordion-body">
                                    {mapFlag && <MapboxDrawLine geoData={geoData} />}
                                </div>
                            </div>
                        </div>
                        <div className="accordion-item">
                            <h2 className="accordion-header">
                                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseThree" aria-expanded="false" aria-controls="panelsStayOpen-collapseThree">
                                    Add Description
                                </button>
                            </h2>
                            <div id="panelsStayOpen-collapseThree" className="accordion-collapse collapse">
                                <div className="accordion-body">
                                    <div className="container text-center">
                                        <form onSubmit={upload}>
                                            <div className="form-group">
                                                <div className="col">
                                                    <div className="row d-flex justify-content-center">
                                                        <label className="col-sm-1 control-label d-flex align-items-center">Time:</label>
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
                                                <div className="col">
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
                                                <label className="control-label col-sm-2" htmlFor="description">Comment:</label>
                                                <div className="col">
                                                    <textarea className="form-control" rows="5" value={comment} onChange={(e) => setComment(e.target.value)} id="comment"></textarea>
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col">
                                                    <button type="submit" className="btn btn-color btn-default">Share</button>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadRoute;