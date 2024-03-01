import React, { useRef, useEffect } from "react";
import { useDispatch } from 'react-redux'
import { saveCoordinates } from '../redux/coordinates'
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css'
import "../style/map.css";

mapboxgl.accessToken = "put the api key";

const MapboxDrawLine = (geoData) => {
    const lat = geoData.geoData.geometry.location.lat
    const lng = geoData.geoData.geometry.location.lng
    const mapContainerRef = useRef(null);
    const dispatch = useDispatch();

  // Initialize map when component mounts
    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainerRef.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [lng, lat],
            zoom: 14,
        });

        const draw = new MapboxDraw({
            displayControlsDefault: false,
            controls: {
                line_string: true,
                trash: true
            }
        })

        map.addControl(draw, "top-left")

        map.on("load", function () {
            map.on('draw.create', updateLine);
            map.on('draw.delete', updateLine);
            map.on('draw.update', updateLine);
        })

        const updateLine = () => {
            const data = draw.getAll();
            console.log(data)
            dispatch(saveCoordinates(data.features[0].geometry.coordinates))
        }
        return () => map.remove();
    }, []);

    return <div className="map-container" ref={mapContainerRef} />;
};

export default MapboxDrawLine;