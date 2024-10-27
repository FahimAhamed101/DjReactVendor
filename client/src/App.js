import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './containers/Home';
import Register from './views/auth/Register'
import Login from './views/auth/Login'
import StoredHeader from './views/base/StoredHeader'
import MainWrapper from './views/base/MainWrapper'
function App() {
  return (
    <Router>
     <StoredHeader />
     <MainWrapper>
        <Routes>
        <Route path="/" element={<Home />} />
                          
                          
                          
        <Route path='/register' element={<Register />} />
        <Route path="/login" element={<Login />} />

        </Routes> 
         </MainWrapper>
     </Router>
   
  );
}

export default App;
