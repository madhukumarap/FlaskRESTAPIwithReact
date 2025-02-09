import React, { useState,useEffect } from "react";
import ReactDOM from "react-dom/client";
import 'bootstrap/dist/css/bootstrap.min.css';
import NavBar from "./components/NavBar";
import {
  BrowserRouter as Router,
  Switch, Route
} from "react-router-dom"
const App = () => {
  useEffect(() => {
    fetch("http://localhost:5000/hello")
      .then((response) => {
        console.log("Response received:", response); // Debugging
       
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Data:", data)
        setMessage(data.message)
      })
      .catch((error) => console.error("Fetch error:", error));

  }, []);
  
  
  const [message, setMessage] = useState("Hello, React!");
  return (
    <div>
      <NavBar/>
    </div>
  );
};

// Use createRoot instead of render
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
