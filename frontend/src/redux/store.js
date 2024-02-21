import { configureStore } from '@reduxjs/toolkit'
import loginStatusReducer from './loginStatus'
import userInfoReducer from './userInfo'

export default configureStore({
    reducer: {
        loginStatus: loginStatusReducer,
        userInfo:userInfoReducer
    }
})

