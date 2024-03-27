// RouteSearch.js
import React, { useEffect, useState } from 'react';
import '../style/routesearch.css'

const RouteSearch = ({ onSearch }) => {
    // State variables to store filter criteria
    const [city, setCity] = useState('');
    const [location, setLocation] = useState('');
    const [difficulty, setDifficulty] = useState('');
    const [mobility, setMobility] = useState('');
    const [comment, setComment] = useState('');
    const [distance, setDistance] = useState(0);
    const [distanceMargin, setDistanceMargin] = useState(0);
    const [creatorUsername, setCreatorUsername] = useState('');
    const [minutes, setMinutes] = useState(0);
    const [timeMargin, setTimeMargin] = useState(0);
    const [reload, setReload] = useState(false);
    const [expanded, setExpanded] = useState(false);

    const toggleForm = () => {
        setExpanded(!expanded);
    };

    const handleSearch = (e) => {
        e.preventDefault();
        const searchParams = {
            city: city.trim() !== '' ? city : undefined,
            location: location.trim() !== '' ? location : undefined,
            difficulty: difficulty.trim() !== '' ? difficulty : undefined,
            mobility: mobility.trim() !== '' ? mobility : undefined,
            comment: comment.trim() !== '' ? comment : undefined,
            distance: parseInt(distance) !== 0 ? parseFloat(distance) : undefined,
            distanceMargin: parseInt(distanceMargin) !== 0 ? parseFloat(distanceMargin) : undefined, 
            creator_username: creatorUsername.trim() !== '' ? creatorUsername : undefined,
            minutes: parseInt(minutes) !== 0 ? parseInt(minutes) : undefined,
            timeMargin: parseInt(timeMargin) !== 0 ? parseInt(timeMargin) : undefined,
        };
        onSearch(searchParams);
    };

    const resetForm = () => {
        setCity('');
        setLocation('');
        setDifficulty('');
        setMobility('');
        setComment('');
        setDistance(0);
        setDistanceMargin(0);
        setCreatorUsername('');
        setMinutes(0);
        setTimeMargin(0);
        setReload(!reload);
    };

    useEffect(() => {
        console.log('RouteSearch.js: useEffect');
    }, [reload]);

    return (
        <div className="route-search">
            <h3 id="search-toggle" onClick={toggleForm}>Route Search 🔎</h3>
            {expanded && (
            <form onSubmit={handleSearch}>
                <div className="form-group">
                    <div className="col">
                        <div className="row d-flex justify-content-center">
                        </div>
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="city">City:</label>
                    <div className="col">
                        <input type="text" className="form-control" id="city" value={city} onChange={(e) => setCity(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="location">Location:</label>
                    <div className="col">
                        <input type="text" className="form-control" id="location" value={location} onChange={(e) => setLocation(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="distance">Distance:</label>
                    <div className="col">
                        <input type="number" className="form-control" id="distance" value={distance} onChange={(e) => setDistance(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="distanceMargin">Margin:</label>
                    <div className="col">
                        <input type="number" className="form-control" id="distanceMargin" value={distanceMargin} onChange={(e) => setDistanceMargin(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="time">Time:</label>
                    <div className="col">
                        <input type="number" className="form-control" id="time" value={minutes} onChange={(e) => setMinutes(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="timeMargin">Margin:</label>
                    <div className="col">
                        <input type="number" className="form-control" id="timeMargin" value={timeMargin} onChange={(e) => setTimeMargin(e.target.value)} />
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
                    <label className="control-label col-sm-2">Mobility:</label>
                    <div className="col">
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="inlineRadioOptions2" id="inlineRadio21" value="Walk" onChange={(e) => setMobility(e.target.value)} />
                            <label className="form-check-label" htmlFor="inlineRadio1">Walk</label>
                        </div>
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="inlineRadioOptions2" id="inlineRadio22" value="Run" onChange={(e) => setMobility(e.target.value)} />
                            <label className="form-check-label" htmlFor="inlineRadio2">Run</label>
                        </div>
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="inlineRadioOptions2" id="inlineRadio23" value="Bike" onChange={(e) => setMobility(e.target.value)} />
                            <label className="form-check-label" htmlFor="inlineRadio3">Bike</label>
                        </div>
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="inlineRadioOptions2" id="inlineRadio24" value="All" onChange={(e) => setMobility(e.target.value)} />
                            <label className="form-check-label" htmlFor="inlineRadio4">All</label>
                        </div>
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="creatorUsername">Creator:</label>
                    <div className="col">
                        <input type="text" className="form-control" id="creatorUsername" value={creatorUsername} onChange={(e) => setCreatorUsername(e.target.value)} />
                    </div>
                </div>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="description">Comment:</label>
                    <div className="col">
                        <textarea className="form-control commentbox" rows="5" value={comment} onChange={(e) => setComment(e.target.value)} id="comment"></textarea>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        <button type="submit" className="btn btn-color btn-default" id="sharebtn">Search</button>
                    </div>
                    <div className="col">
                        <button type="button" className="btn btn-secondary" onClick={resetForm}>Reset</button>
                    </div>
                </div>
            </form>
             )}
        </div>
    );
};

export default RouteSearch;