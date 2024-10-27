import React, { useContext, useEffect, useState } from 'react';

import { Link } from 'react-router-dom';


import { styled } from '@mui/material';

const Home = () => {


    return (
        <div>
            <div className='container'>
               
                        <>
                        <div className="row mt-3">
                            <h3 className='mb-4'>
                                Latest Products
                                <Link to="/" className='float-end btn btn-sm' style={{backgroundColor:"darkslategrey",color:"white"}}>
                                    View All Products <i className='fa-solid fa-arrow-right-long'></i>
                                </Link>
                            </h3>
                            <div className="row">
                           
                            </div>
                        </div>
                        <h3 className='mb-4'>
                            Popular Categories
                            <Link to="/" className='float-end btn btn-sm' style={{backgroundColor:"darkslategrey",color:"white"}}>
                                View All Categories <i className='fa-solid fa-arrow-right-long'></i>
                            </Link>
                        </h3>
                        <div className="row">
                        
                                <div className="col-12 col-md-3 mb-4" >
                                    <Link style={{ color: "initial", textDecoration: 'none' }} to='/'>
                                        <div className="card fixed-size-card">
                                            <img src='' className='card-img-top large-image' alt='' />
                                            <div className="card-body card-background">
                                                <h4 className="card-title">Title: </h4>
                                                <p className="card-text">Description: </p>
                                            </div>
                                            <div className="card-footer">
                                                <h5 className='card-text text-muted'>Product Downloads: 5432</h5>
                                            </div>
                                        </div>
                                    </Link>
                                </div>
                        
                        </div>
                        <h3 className='mb-4'>
                            Popular Products
                            <Link to="/" className='float-end btn btn-sm' style={{backgroundColor:"darkslategrey",color:"white"}}>
                                View All Popular Products <i className='fa-solid fa-arrow-right-long'></i>
                            </Link>
                        </h3>
                        <div className="row">
                          
                                <div className="col-12 col-md-3 mb-4" >
                                <Link to={`/product/`} style={{textDecoration:"none" ,color:"black"}}>
                                    <div className="card fixed-size-card">
                                        <img src='' className='card-img-top large-image' alt="image9" />
                                        <div className="card-body">
                                            <h4 className="card-title">title</h4>
                                           
                                               
                                                    <h5 className='card-title text-muted'>Price: $ 200</h5>
                                               
                                            
                                        </div>
                                        <div className="card-footer">
                                            <button title='Add to Cart' className='btn btn-success btn-sm'>
                                                <i className='fa-solid fa-cart-plus'></i>
                                            </button>
                                            <button className="btn btn-danger btn-sm ms-1" title="Add to Wishlist">
                                                <i className='fa fa-heart'></i>
                                            </button>
                                        </div>
                                    </div>
                                </Link>
                                </div>
                    
                        </div>
                        <h3 className='mb-4'>
                            Popular Sellers
                            <Link to="/seller" className='float-end btn btn-sm' style={{backgroundColor:"darkslategrey",color:"white"}}>
                                View All Sellers <i className='fa-solid fa-arrow-right-long'></i>
                            </Link>
                        </h3>
                        <div className="row">
                               
                                        <div className="col-12 col-md-3 mb-5" >
                                            <Link to='/seller/product/' style={{textDecoration:'none'}}>
                                                <div className="card fixed-size-card text-center">
                                                    <img src="" className='card-img-top large-image' alt="image13" />
                                                    <div className="card-body" style={{color:"black"}}>
                                                        <h5>Seller Name : name</h5>
                                                    </div>
                                                    <div className="card-footer" style={{color:"black"}}>
                                                        Categories : <Link to="/">Python</Link> , <Link href='/'>Java</Link>
                                                    </div>
                                                </div>
                                            </Link>
                                        </div>
                                  
                        </div>
                        </>
                 
            </div>
        </div>
    );
};

export default Home;