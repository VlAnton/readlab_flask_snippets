import React from 'react';
import {
    BrowserRouter as Router, Switch, Redirect, Route,
} from 'react-router-dom';

import App from './components/app/app';
import ListPage from './pages/list-page/list-page';
import DetailPage from './pages/detail-page/detail-page'
import CreatePage from './pages/create-page/create-page'


class AppRouter extends React.Component {
    render() {
        return (
            <Router>
                <App>
                    <Switch>
                        <Redirect exact from="/" to="/list" />
                        <Route path="/list" component={ListPage} />
                        <Route path="/snippets/:uid" component={DetailPage} />
                        <Route path="/create" component={CreatePage} />
                    </Switch>
                </App>
            </Router>
        );
    }
}

export default AppRouter;