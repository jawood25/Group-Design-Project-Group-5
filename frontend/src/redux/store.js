import { configureStore } from '@reduxjs/toolkit'
import loginStatusReducer from './loginStatus'
import userInfoReducer from './userInfo'
import coordinatesReducer from './coordinates'

export default configureStore({
    reducer: {
        loginStatus: loginStatusReducer,
        userInfo:userInfoReducer,
        coordinates: coordinatesReducer
    }
})

