import React, { useRef, useEffect, useState } from "react";
import { useDispatch } from 'react-redux';
import { saveCoordinates } from '../redux/coordinates';
import { saveMapCenter } from '../redux/mapCenter';
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css';
import "../style/map.css";

mapboxgl.accessToken = "";

const EditRoute = ({route}) => {
    const mapContainerRef = useRef(null);
    const dispatch = useDispatch();

    useEffect(() => {
        const map = new mapboxgl.Map({
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
            // Add a symbol layer
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

        return () => map.remove();
    }, []); 

    return <div className="map-container" ref={mapContainerRef} />;
};

export default EditRoute;