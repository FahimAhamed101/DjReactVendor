import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Products from './views/store/Products'
import Register from './views/auth/Register'
import Login from './views/auth/Login'
import Logout from './views/auth/Logout'
import ForgetPassword from './views/auth/ForgetPassword'
import CreatePassword from './views/auth/CreatePassword'
import Account from './views/customer/Account'
import StoredHeader from './views/base/StoredHeader'
import MainWrapper from './views/base/MainWrapper'
function App() {
  return (
    <Router>
     <StoredHeader />
     <MainWrapper>
        <Routes>
        <Route path='/' element={<Products />} />
                          
                          
                          
        <Route path='/register' element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path='/logout' element={<Logout />} />
        <Route path='/forget-password' element={<ForgetPassword />} />
        <Route path='/create-new-password' element={<CreatePassword />} />
        <Route path='/customer/account/' element={<Account />} />
        </Routes> 
         </MainWrapper>
     </Router>
   
  );
}

export default App;
