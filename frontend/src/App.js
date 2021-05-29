import './App.css';

import Home from './screens/HomeScreen';
import About from './screens/AboutScreen';
import Analysis from './screens/AnalysisScreen';

import Navbar from './components/Navbar';
import Footer from './components/Footer';

import { Route } from 'react-router-dom';

function App() {

  return (
    <div className="container">
      <Navbar/>
      <Route exact path="/" component={Home}/>
      <Route exact path="/about" component={About} />
      <Route exact path="/analyze" component={Analysis} />
      <Footer/>
    </div>
  );
}

export default App;
