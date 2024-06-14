import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Main from './pages/Main';
import Error from './pages/Error';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import MyAccount from './pages/MyAccount';
import Community from './pages/Community';
import MapboxRenderLine from './pages/MapboxRenderLine'
import UploadRoute from './pages/UploadRoute'
import './style/style.css';
import store from './redux/store';
import { Provider } from 'react-redux';
import Profile from './components/Profile';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Main />,
    errorElement: <Error />
  },
  {
    path: "sign-up",
    element: <SignUp />
  },
  {
    path: "login",
    element: <Login />
  },
  {
    path: "my-account",
    element: <MyAccount />
  },
  {
    path: "/mapbox-render-line",
    element: <MapboxRenderLine />
  },
  {
    path: "/upload-route",
    element: <UploadRoute />
  },
  {
    path: "/community",
    element: <Community />
  },
  {
    path: "/profile/:friend_username",
    element: <Profile />
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />  
    </Provider>
  </React.StrictMode>
);
