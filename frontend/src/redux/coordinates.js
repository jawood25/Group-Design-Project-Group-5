import { createSlice } from '@reduxjs/toolkit';

export const coordinates = createSlice({
    name: 'coordinates',
    initialState: {
        coordinates: []
    },
    reducers: {
        saveCoordinates: (state, action) => {
            state.coordinates = action.payload;
        }
    }
});

export const { saveCoordinates } = coordinates.actions

export default coordinates.reducer