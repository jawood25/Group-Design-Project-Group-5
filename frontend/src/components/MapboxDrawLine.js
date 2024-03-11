import React, { useRef, useEffect } from "react";
import { useDispatch } from 'react-redux'
import { saveCoordinates } from '../redux/coordinates'
import { saveMapCenter } from '../redux/mapCenter'
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css'
import "../style/map.css";

mapboxgl.accessToken = "pk.eyJ1Ijoic29ub2RhbSIsImEiOiJjbHQ4bnNhM2cwNm4yMmttc2ljc2tuenA1In0.fBw9Dz2FIxgEMMFakE_VmQ";

const MapboxDrawLine = (geoData) => {
    const lat = geoData.geoData.geometry.location.lat
    const lng = geoData.geoData.geometry.location.lng
    const mapContainerRef = useRef(null);
    const dispatch = useDispatch();

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
            if(data.features.length > 0) {
                dispatch(saveCoordinates(data.features[0].geometry.coordinates))
                const mapCenter = map.getCenter()
                dispatch(saveMapCenter({ lat: mapCenter.lat, lng: mapCenter.lng }))
            }
        }
        return () => map.remove();
    }, []);

    return <div className="map-container" ref={mapContainerRef} />;
};

export default MapboxDrawLine;