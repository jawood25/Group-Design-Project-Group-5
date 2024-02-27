import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Main from './pages/Main';
import Error from './pages/Error';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import MyAccount from './pages/MyAccount';
import Map from './components/Map';
import Upload from './pages/Upload';
import './style/style.css';
import store from './redux/store';
import { Provider } from 'react-redux';

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
    path: "/test-map",
    element: <Map />
  },
  {
    path: "/upload",
    element: <Upload />
  }
  // {
  //   path: "/test-map-npm",
  //   element: <MapNpm />
  // }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />  
    </Provider>
  </React.StrictMode>
);
