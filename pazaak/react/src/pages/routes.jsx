import React from 'react';
import { Route } from 'react-router';
import { BrowserRouter } from 'react-router-dom';
import PlayPage from './PlayPage';
import LoginPage from './LoginPage';
import CreateAccountPage from './CreateAccountPage';


export default function() {
    return (
        <BrowserRouter>
            <Route path="/play" component={PlayPage} />
            <Route path="/login" component={LoginPage} />
            <Route path="/create-account" component={CreateAccountPage} />
        </BrowserRouter>
    );
}