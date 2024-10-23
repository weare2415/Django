import React from 'react'
import ReactDOM from 'react-dom'
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
} from 'react-router-dom'

import './style.css'
import RecommandPage from './views/recommand-page'
import Home from './views/home'
import SignUpPage from './views/sign-up-page'
import DestinationPage from './views/destination-page'
import LoginPage from './views/login-page'
import ReviewPage from './views/review-page'
import NotFound from './views/not-found'

const App = () => {
  return (
    <Router>
      <Switch>
        <Route component={RecommandPage} exact path="/recommand-page" />
        <Route component={Home} exact path="/" />
        <Route component={SignUpPage} exact path="/sign-up-page" />
        <Route component={DestinationPage} exact path="/destination-page" />
        <Route component={LoginPage} exact path="/login-page" />
        <Route component={ReviewPage} exact path="/review-page" />
        <Route component={NotFound} path="**" />
        <Redirect to="**" />
      </Switch>
    </Router>
  )
}

ReactDOM.render(<App />, document.getElementById('app'))
