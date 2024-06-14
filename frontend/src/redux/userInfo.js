import { createSlice } from '@reduxjs/toolkit';

export const userInfo = createSlice({
    name: 'userInfo',
    initialState: {
        username: ""
    },
    reducers: {
        saveUsername: (state, action) => {
            state.username = action.payload;
        }
    }
});

export const { saveUsername } = userInfo.actions

export default userInfo.reducer