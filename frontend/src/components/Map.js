import { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';

const Map = () => { 
    const username = useSelector((state) => state.userInfo.username)
    const initialFlag = useRef(true);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch('/api/userroutes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }),
                });
                if (!response.ok) {
                    throw new Error('fetch api failed');
                }
                const data = await response.json();
                console.log(data);
                console.log("Data fetched successfully");
                data.routes.forEach((route, index) => {
                    const mapContainer = document.createElement('div'); 
                    mapContainer.id = `map${index}`; 
                    mapContainer.style.height = '400px'; 
                    mapContainer.style.width = '800px';
                    mapContainer.style.overflow = 'hidden';
                    mapContainer.style.float = 'left';
                    mapContainer.style.border = 'thin solid #333';
                    document.querySelector('.Map').appendChild(mapContainer);
                    console.log(document.querySelector('.Map'))

                    const map = new window.google.maps.Map(mapContainer, { 
                        center: { lat: 53.3437935, lng: -6.2545716 },
                        zoom: 16,
                        mapTypeId: 'terrain',
                        streetViewControl: false
                    });

                    const kmlLayer = new window.google.maps.KmlLayer(route.kmlURL, { // ルートごとにKMLレイヤーを追加
                        suppressInfoWindows: true,
                        preserveViewport: false,
                        map: map
                    });
                });
            } catch (error) {
                console.error('fetch api failed 2', error);
            }
        };

        if (initialFlag.current) {
            fetchUserData(); 
            initialFlag.current = false;
        }
        
    }, [username])

    return (
        <div className='Map'></div> 
    )
};

export default Map;
