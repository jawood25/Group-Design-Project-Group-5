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
        }
    }
});

export const { saveMapCenter } = mapCenter.actions

export default mapCenter.reducer