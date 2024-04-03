import React, { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import { useSelector } from 'react-redux';
import '../style/mainmap.css'

mapboxgl.accessToken = "pk.eyJ1Ijoic29ub2RhbSIsImEiOiJjbHQ4bnNhM2cwNm4yMmttc2ljc2tuenA1In0.fBw9Dz2FIxgEMMFakE_VmQ";

const MainMap = ({ allUR }) => {
    const username = useSelector((state) => state.userInfo.username)
    const [lat, setLat] = useState('53.343575');
    const [lng, setLng] = useState('-6.255069');
    const mapContainerRef = useRef(null);
    const colorList = ["#F44336", "#E91E63", "#9C27B0", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#FFC107", "#FF9800"];

    useEffect(() => {
        if (allUR) {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    setLat(position.coords.latitude);
                    setLng(position.coords.longitude);
                }, function (error) {
                    console.error("Error getting geolocation:", error);
                });
            } else {
                console.error("Geolocation is not supported by this browser.");
            }
            const map = new mapboxgl.Map({
                container: mapContainerRef.current,
                style: 'mapbox://styles/mapbox/streets-v12',
                center: [lng, lat],
                zoom: 13,
            });

            map.on("load", function () {
                allUR.forEach(route => {
                    const sourceId = `route-${route.id}`;
                    const layerId = `route-${route.id}-layer`;

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

                    map.on("click", layerId, function (e) {
                        const coordinates = e.lngLat;
                        const description = `<strong style="font-size: 16px; padding: 0 5px;">Route by ${route.creator_username} </strong><p style="margin-bottom: 5px;"></p>
                                            <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">Distance: ${route.distance} km</p>
                                            <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">${route.mobility}: ${route.minutes} minutes</p>
                                            <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">Difficulty: ${route.difficulty}</p>
                                            <p style="font-size: 14px; margin-bottom: 0; padding: 0 5px;">Likes: ${route.saves}</p>`;

                        const popup = new mapboxgl.Popup()
                            .setLngLat(coordinates)
                            .setHTML(description)
                            .addTo(map);

                        const likeButton = document.createElement("button");
                        likeButton.classList.add("like-button");
                        likeButton.textContent = "Like";
                        likeButton.style.marginTop = "5px";

                        likeButton.addEventListener("click", (event) => {
                            event.stopPropagation(); // Prevent click propagation to avoid triggering map click event
                            likeRoute(route.id); // Call your likeRoute function with the route ID
                        });

                        popup._content.appendChild(likeButton);
                        popup._content.style.cursor = "default";
                    });

                    map.on("mouseenter", layerId, function () {
                        map.getCanvas().style.cursor = "pointer";
                    });

                    map.on("mouseleave", layerId, function () {
                        map.getCanvas().style.cursor = "";
                    });
                });
            });

            return () => {
                map.remove();
            };
        }
    }, [lat, lng, allUR]);

    const likeRoute = (route_id) => {
        console.log("Route liked:", route_id);
        fetch("/api/savingroutes/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ route_id, username }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Route liked:", data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
    };

    return <div className="map-container" ref={mapContainerRef} />;
};

export default MainMap;