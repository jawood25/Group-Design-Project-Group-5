import React, { useRef, useEffect, useState } from "react";
import { useDispatch } from 'react-redux';
import { saveCoordinates } from '../redux/coordinates';
import { saveMapCenter } from '../redux/mapCenter';
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css';
import "../style/map.css";

mapboxgl.accessToken = "pk.eyJ1Ijoic29ub2RhbSIsImEiOiJjbHQ4bnNhM2cwNm4yMmttc2ljc2tuenA1In0.fBw9Dz2FIxgEMMFakE_VmQ";

const EditRoute = ({route}) => {
    const mapContainerRef = useRef(null);
    const dispatch = useDispatch();

    useEffect(() => {
        let map;
        const timeoutId = setTimeout(() => {
            map = new mapboxgl.Map({
                container: mapContainerRef.current,
                style: 'mapbox://styles/mapbox/streets-v12',
                center: [route.map_center.lng, route.map_center.lat],
                zoom: 14,
            });
    
            const draw = new MapboxDraw({
                displayControlsDefault: false,
                controls: {
                    line_string: true,
                    trash: true
                }
            });
    
            map.addControl(draw, "top-left");
    
            map.on("load", function () {
                map.addSource("route", {
                    type: "geojson",
                    data: {
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: 'LineString',
                            coordinates: route.coordinates
                        }
                    },
                });
                map.addLayer({
                    id: "route",
                    type: "line",
                    source: "route",
                    layout: {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    paint: {
                        'line-color': '#888',
                        'line-width': 4
                    }
                });
    
                map.on('draw.create', updateLine);
                map.on('draw.delete', updateLine);
                map.on('draw.update', updateLine);
            });
    
            const updateLine = () => {
                const data = draw.getAll();
                if(data.features.length > 0) {
                    dispatch(saveCoordinates(data.features[0].geometry.coordinates));
                    const mapCenter = map.getCenter();
                    dispatch(saveMapCenter({ lat: mapCenter.lat, lng: mapCenter.lng }));
                }
            };
    
        }, 2000)
        return () => {
            clearTimeout(timeoutId);
            if (map) map.remove();
        };
    }, [route]); 

    return <div className="map-container" ref={mapContainerRef} style={{ width: "700px", height: "400px" }}/>;
};

export default EditRoute;