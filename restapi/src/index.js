import React, { useState,useEffect } from "react";
import ReactDOM from "react-dom/client";
import 'bootstrap/dist/css/bootstrap.min.css';
import NavBar from "./components/NavBar";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom'
import HomePage from './components/Home';
import SignUpPage from './components/SignUp';
import LoginPage from './components/Login';
import CreateRecipePage from './components/CreateRecipe';




const App=()=>{

  
  return (
      <Router>
      <div className="">
          <NavBar/>
          <Switch>
              <Route path="/create_recipe">
                  <CreateRecipePage/>
              </Route>
              <Route path="/login">
                  <LoginPage/>
              </Route>
              <Route path="/signup">
                  <SignUpPage/>                
              </Route>    
              <Route path="/">
                  <HomePage/>
              </Route>
          </Switch>
      </div>
      </Router>
  )
}

// Use createRoot instead of render
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
