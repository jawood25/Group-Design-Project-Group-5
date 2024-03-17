import React, { useRef, useEffect,useState } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "pk.eyJ1Ijoic29ub2RhbSIsImEiOiJjbHQ4bnNhM2cwNm4yMmttc2ljc2tuenA1In0.fBw9Dz2FIxgEMMFakE_VmQ";

const MainMap = ({allUR}) => {
    const [lat, setLat] = useState('53.343575');
    const [lng, setLng] = useState('-6.255069');
    const mapContainerRef = useRef(null);
    const colorList = ["#F44336", "#E91E63", "#9C27B0", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#FFC107", "#FF9800"]

  // Initialize map when component mounts
    useEffect(() => {
        if (allUR) {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    setLat(position.coords.latitude);
                    setLng(position.coords.longitude);
                }, function(error) {
                    console.error("Error getting geolocation:", error);
                });
            } else {
                console.error("Geolocation is not supported by this browser.");
            }
            const map = new mapboxgl.Map({
                container: mapContainerRef.current,
                style: 'mapbox://styles/mapbox/streets-v12',
                center: [lng,lat],
                zoom: 13,
            });
    
            map.on("load", function () {
                console.log(allUR)
                allUR.forEach(route => {
                            console.log(route)
                            const sourceId = `route-${route.id}`;
                            const layerId = `route-${route.id}-layer`;
                            console.log(sourceId)


                            map.addSource(sourceId, {
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

                            const randomColor = colorList[Math.floor(Math.random() * colorList.length)];
                            // Add a symbol layer
                            map.addLayer({
                                id: layerId,
                                type: "line",
                                source: sourceId,
                                layout: {
                                    'line-join': 'round',
                                    'line-cap': 'round'
                                },
                                paint: {
                                    'line-color': randomColor,
                                    'line-width': 4
                                }
                            });
                            // Add click event listener to the line layer
                            map.on("click", layerId, function (e) {
                                const coordinates = e.lngLat;
                                const description = `<strong style="font-size: 16px; padding: 0 5px;">Route by ${route.creator_username} </strong><p style="margin-bottom: 5px;"></p>
                                                    <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">Distance: ${route.distance} km</p>
                                                    <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">${route.mobility}: ${route.minutes} minutes</p>
                                                    <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">Difficulty: ${route.difficulty}</p>
                                                    `;
                                new mapboxgl.Popup()
                                    .setLngLat(coordinates)
                                    .setHTML(description)
                                    .addTo(map);
                            });
                
                            // Change the cursor to a pointer when hovering over the line layer
                            map.on("mouseenter", layerId, function () {
                                map.getCanvas().style.cursor = "pointer";
                            });
                
                            // Change it back to the default cursor when it leaves
                            map.on("mouseleave", layerId, function () {
                                map.getCanvas().style.cursor = "";
                            });
                });
            });
    
            return () => {
                map.remove();
            };
        }
    }, [lat, lng,allUR]);

    return <div className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "100vh" }}/>;
};

export default MainMap;