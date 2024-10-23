import React from 'react'

import { Helmet } from 'react-helmet'

import SignInPage from '../components/sign-in-page'
import './loginpage.css'

const LoginPage = (props) => {
  return (
    <div className="login-page-container">
      <Helmet>
        <title>LoginPage - Travel_Webapp</title>
        <meta property="og:title" content="LoginPage - Travel_Webapp" />
      </Helmet>
      <SignInPage></SignInPage>
    </div>
  )
}

export default LoginPage
