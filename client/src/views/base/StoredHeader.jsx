import React, {useState, useContext} from 'react'
import { Link, useNavigate } from 'react-router-dom'
import  useAuthStore  from '../../store/auth'




function StoredHeader() {

    const [isLoggedIn, user] = useAuthStore((state) => [
        state.isLoggedIn,
        state.user
    ])

    console.log(isLoggedIn())




    //console.log(cartCount)

 
    const navigate=useNavigate()



  return (
    <div><nav className="navbar navbar-expand-lg navbar-dark bg-dark">
    <div className="container">
        <Link className="navbar-brand" to="/">My Shop </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
     

            {/* <Link className="btn btn-primary me-2" to="/login">Login</Link>
            <Link className="btn btn-primary me-2" to="/register">Register</Link> */}


            {/* These are the button rendered based on users logged in status */}
            {/* You could just un-comment it ;) */}

            {isLoggedIn()
                ?
                <>
                    <Link className="btn btn-primary me-2" to={'/customer/account/'}>Account</Link>
                    <Link className="btn btn-primary me-2" to="/logout">Logout</Link>
                </>
                :
                <>
                    <Link className="btn btn-primary me-2" to="/login">Login</Link>
                    <Link className="btn btn-primary me-2" to="/register">Register</Link>

                </>
            }
            <Link className="btn btn-danger" to="/cart/"><i className='fas fa-shopping-cart'></i> <span id='cart-total-items'>1</span></Link>

        </div>
    </div>
</nav></div>
  )
}

export default StoredHeader