import { createSlice } from '@reduxjs/toolkit';

export const coordinates = createSlice({
    name: 'coordinates',
    initialState: {
        coordinates: []
    },
    reducers: {
        saveCoordinates: (state, action) => {
            state.coordinates = action.payload;
        },
        resetCoordinates: state => {
            state.coordinates = [];
        }
    }
});

export const { saveCoordinates, resetCoordinates } = coordinates.actions

export default coordinates.reducer