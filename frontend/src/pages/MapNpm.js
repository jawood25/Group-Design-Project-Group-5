import Header from '../components/Header';
import { useState } from 'react';
import { APIProvider, Map, Marker} from '@vis.gl/react-google-maps';

const MapNpm = () => {
    return (
        <div className='MapNpm'>
            <Header />
            <h2>Map with Npm</h2>
            <APIProvider apiKey=''>
                <div style={{ height: "400px", width: "800px" }}>
                    <Map
                        defaultCenter={{ lat: 53.3437935, lng: -6.2545716 }}
                        defaultZoom={15}
                        gestureHandling={'greedy'}
                    >
                    <Marker position={{lat: 53.3437935, lng: -6.2545716}} />
                    </Map>
                </div>
            </APIProvider>
        </div>
    );
};

export default MapNpm;