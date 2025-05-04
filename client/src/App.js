import { useEffect, useState } from 'react'
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
import ProductDetail from './views/store/ProductDetail'
import PrivateRoute from './layout/PrivateRoute'
import Dashboard from './views/vendor/Dashboard'
import Cart from './views/store/Cart'
import { CartContext } from './views/plugin/Context'
import CartID from './views/plugin/CartID'
import UserData from './views/plugin/UserData'
import apiInstance from "./utils/axios";
import Search from './views/store/Search'
function App() {

 const [count, setCount] = useState(0)
  const [cartCount, setCartCount] = useState()

  const cart_id = CartID()
  const userData = UserData()

  useEffect(() => {
    const url = userData ? `cart-list/${cart_id}/${userData?.user_id}/` : `cart-list/${cart_id}/`
        apiInstance.get(url).then((res) => {
          console.log(res.data)
          setCartCount(res.data.length)

        })
            

  })

  return (
    <CartContext.Provider value={[cartCount, setCartCount]}>
    <Router>
     <StoredHeader />
     <MainWrapper>
        <Routes>
        <Route path='/' element={<Products />} />
                          
        <Route path="/detail/:slug/" element={<ProductDetail />} /> 
        <Route path='/cart' element={<Cart />} />                 
        <Route path='/register' element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path='/logout' element={<Logout />} />
        <Route path='/forget-password' element={<ForgetPassword />} />
        <Route path='/create-new-password' element={<CreatePassword />} />
        <Route path='/customer/account/' element={<Account />} />
        <Route path='/vendor/dashboard/' element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path='/search/' element={<Search />} />
        </Routes> 
         </MainWrapper>
     </Router>
     </CartContext.Provider>
  );
}

export default App;
