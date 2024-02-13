import React from 'react';
import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Main from './pages/Main';
import Error from './pages/Error';
import SignUp from './pages/SignUp'
import Login from './pages/Login'

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
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
