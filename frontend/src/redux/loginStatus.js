import { createSlice } from '@reduxjs/toolkit';

export const loginStatus = createSlice({
    name: 'loginStaus',
    initialState: {
        isLoggedIn: false
    },
    reducers: {
        login: (state) => {
            state.isLoggedIn = true;
        },
        logout: (state) => {
            state.isLoggedIn = false;
        }
    }
});

export const { login, logout } = loginStatus.actions

export default loginStatus.reducer