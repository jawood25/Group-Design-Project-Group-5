import { configureStore } from '@reduxjs/toolkit'
import loginStatusReducer from './loginStatus'
import userInfoReducer from './userInfo'
import coordinatesReducer from './coordinates'
import mapCenterReducer from './mapCenter'

export default configureStore({
    reducer: {
        loginStatus: loginStatusReducer,
        userInfo: userInfoReducer,
        coordinates: coordinatesReducer,
        mapCenter: mapCenterReducer
    }
})

