import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, HashRouter } from 'react-router-dom';
import { App } from './App';
import { isStaticDataMode } from './config/dataMode';
import './index.css';

const Router = isStaticDataMode ? HashRouter : BrowserRouter;

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router basename={isStaticDataMode ? undefined : import.meta.env.BASE_URL}>
      <App />
    </Router>
  </React.StrictMode>,
);
