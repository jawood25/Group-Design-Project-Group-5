import React, { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "../style/map.css";

mapboxgl.accessToken = "";

const MapboxRenderLine = (route) => {
    const mapContainerRef = useRef(null);

  // Initialize map when component mounts
    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainerRef.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [route.route.map_center.lng, route.route.map_center.lat],
            zoom: 14,
        });

        map.on("load", function () {
            map.addSource("route", {
                type: "geojson",
                data: {
                    type: "Feature",
                    properties: {},
                    geometry: {
                        type: 'LineString',
                        coordinates: route.route.coordinates
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
                    'line-color': '#F44336',
                    'line-width': 3
                }
            });
        });

        return () => {
            map.remove();
        };

    }, []);

    return <div className="map-container" ref={mapContainerRef} />;
};

export default MapboxRenderLine;