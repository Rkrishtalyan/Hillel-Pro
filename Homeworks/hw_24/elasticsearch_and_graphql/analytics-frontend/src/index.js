import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {ApolloProvider} from "@apollo/client";
import client from './apolloClient';
import DataDocuments from './components/DataDocuments';
import Clients from './components/Clients';
import Pets from './components/Pets';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { documentsClient, clientsClient, petsClient } from './apolloClient';


const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
    <React.StrictMode>
        <Router>
            <Routes>
                <Route
                    path="/documents"
                    element={
                    <ApolloProvider client={documentsClient}>
                        <DataDocuments />
                    </ApolloProvider>
                }
                />
                <Route
                    path="/clients"
                    element={
                    <ApolloProvider client={clientsClient}>
                        <Clients />
                    </ApolloProvider>
                }
                />
                <Route
                    path="/pets"
                    element={
                    <ApolloProvider client={petsClient}>
                        <Pets />
                    </ApolloProvider>
                }
                />
            </Routes>
        </Router>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
