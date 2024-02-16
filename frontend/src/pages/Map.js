import Header from '../components/Header';
import { useEffect } from 'react';


const Map = () => {
    useEffect(() => {
        const map1 = new window.google.maps.Map(document.getElementById('map1'), {
            center: { lat: 53.3437935, lng: -6.2545716 },
            zoom: 16,
            mapTypeId: 'terrain',
            streetViewControl: false
        });

        const src1 = 'https://www.google.com/maps/d/u/0/kml?mid=1ffe5YOOBsVC5bw-OmLPSumWbzhREELA&forcekml=1';
        const kmlLayer1 = new window.google.maps.KmlLayer(src1, {
            suppressInfoWindows: true,
            preserveViewport: false,
            map: map1
        });
    }, []);
    return (
        <div className='Map'>
            <Header />
            <h2>Test Rendering Map</h2>
            <div id="map1" style={{ height: '400px', width: '800px', overflow: 'hidden', float: 'left', border: 'thin solid #333' }}></div>
        </div>
    );
};

export default Map;