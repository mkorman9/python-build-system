import React, { Component } from 'react';
import logo from './logo.svg';
import './Style.css';
import { Link } from 'react-router-dom'

class Home extends Component {
  render() {
    return (
      <div className="Main">
        <header className="Main-header">
          <img src={logo} className="Main-logo" alt="logo" />
          <h1 className="Main-title">Welcome to React</h1>
        </header>
        <p className="Main-intro">
            Homepage
            <p><Link to="/about">About</Link></p>
        </p>
      </div>
    );
  }
}

export default Home;
