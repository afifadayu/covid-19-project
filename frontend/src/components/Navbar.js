import React, {Component} from 'react';
import '../css/navbar.css';
import logo from '../img/logo.png';

export default class Navbar extends Component {
  state = {
    toggle: false
  }
  Toggle = () => {
    this.setState({ toggle: !this.state.toggle })
  }
  render() {
    const li = [
      {
        link: "/",
        text: "Home"
      },
      {
        link: "/about",
        text: "About us"
      },
      {
        link: "/analyze",
        text: "Analyze"
      }
    ];
    return (
      <>
        <div className="navbar">
          <button onClick={this.Toggle}>
            <img src={logo} className="my-logo" />
          </button>
          
          <ul className={this.state.toggle ? "links show-nav" : "links"}>
            <img src={logo} className="my-logo"/>
            {
              li.map((objLink, i) => {
                return (<li><a href={objLink.link}>{objLink.text}</a></li>)
              })
            }
          </ul>
        </div>
      </>
    );
  }
}