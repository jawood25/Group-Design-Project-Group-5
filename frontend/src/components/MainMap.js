import React, { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "";

const MainMap = () => {
    const mapContainerRef = useRef(null);

  // Initialize map when component mounts
    useEffect(() => {
        const map = new mapboxgl.Map({
            container: mapContainerRef.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [-6.255069, 53.343575],
            zoom: 12,
        });

        map.on("load", function () {
            map.addSource("route", {
                type: "geojson",
                data: {
                    type: "Feature",
                    properties: {},
                    geometry: {
                        type: 'LineString',
                        coordinates: [
                            [
                                -6.228183334329287,
                                53.344557704957396
                            ],
                            [
                                -6.215259057891529,
                                53.342851662215025
                            ],
                            [
                                -6.212791105607238,
                                53.34118432721914
                            ],
                            [
                                -6.219805285784304,
                                53.337422890255255
                            ],
                            [
                                -6.226364843172405,
                                53.341533309705966
                            ],
                            [
                                -6.227988495990843,
                                53.34254146529159
                            ],
                            [
                                -6.228053442104056,
                                53.3444801590407
                            ]
                        ]
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

            // Add click event listener to the line layer
            map.on("click", "route", function (e) {
                const coordinates = e.lngLat;
                const description = "This is your route.";
                new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML(description)
                    .addTo(map);
            });

            // Change the cursor to a pointer when hovering over the line layer
            map.on("mouseenter", "route", function () {
                map.getCanvas().style.cursor = "pointer";
            });

            // Change it back to the default cursor when it leaves
            map.on("mouseleave", "route", function () {
                map.getCanvas().style.cursor = "";
            });
            
        });

        return () => {
            map.remove();
        };

    }, []);

    return <div className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "100vh" }}/>;
};

export default MainMap;