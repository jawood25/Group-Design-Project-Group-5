import { createSlice } from '@reduxjs/toolkit';

export const mapCenter = createSlice({
    name: 'mapCenter',
    initialState: {
        center: {}
    },
    reducers: {
        saveMapCenter: (state, action) => {
            state.center = {
                lat: action.payload.lat,
                lng: action.payload.lng
            };
        },
        resetMapCenter: state => {
            state.center = {};
        }
    }
});

export const { saveMapCenter, resetMapCenter } = mapCenter.actions

export default mapCenter.reducer