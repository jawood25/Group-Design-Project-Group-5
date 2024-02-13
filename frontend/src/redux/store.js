import { configureStore } from '@reduxjs/toolkit'
import loginStatusReducer from './loginStatus'

export default configureStore({
    reducer: {
        loginStaus: loginStatusReducer
    }
})

