import React, { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "";

const MainMap = ({allUR}) => {
    const mapContainerRef = useRef(null);
    const colorList = ["#F44336", "#E91E63", "#9C27B0", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#FFC107", "#FF9800"]

  // Initialize map when component mounts
    useEffect(() => {
        if (allUR) {
            const map = new mapboxgl.Map({
                container: mapContainerRef.current,
                style: 'mapbox://styles/mapbox/streets-v12',
                center: [-6.255069, 53.343575],
                zoom: 13,
            });
    
            map.on("load", function () {
    
                Object.keys(allUR).forEach(key => {
                    if((allUR[key]).length > 0) {
                        console.log(key)
                        allUR[key].forEach((route) => {
                            console.log(route)

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
                        })
                    }
                });
            });
    
            return () => {
                map.remove();
            };
        }
    }, [allUR]);

    return <div className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "100vh" }}/>;
};

export default MainMap;