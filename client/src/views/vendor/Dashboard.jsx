import React,{useState, useEffect} from 'react'

import Sidebar from './Sidebar'
import {Line, Bar} from 'react-chartjs-2'
import { Chart } from 'chart.js/auto'
import { Link } from 'react-router-dom'

function Dashboard() {

    return (
        <div className="container-fluid" id="main">
        <div className="row row-offcanvas row-offcanvas-left h-100">
          {/* Add Side Bar Here */}
          
          <Sidebar /> 
          
          <div className="col-md-9 col-lg-10 main mt-4">
            <div className="row mb-3">
              <div className="col-xl-3 col-lg-6 mb-2">
                <div className="card card-inverse card-success">
                  <div className="card-block bg-success p-3">
                    <div className="rotate">
                      <i className="bi bi-grid fa-5x" />
                    </div>
                    <h6 className="text-uppercase">Products</h6>
                 
                  </div>
                </div>
              </div>
              <div className="col-xl-3 col-lg-6 mb-2">
                <div className="card card-inverse card-danger">
                  <div className="card-block bg-danger p-3">
                    <div className="rotate">
                      <i className="bi bi-cart-check fa-5x" />
                    </div>
                    <h6 className="text-uppercase">Orders</h6>
                
                  </div>
                </div>
              </div>
            
              <div className="col-xl-3 col-lg-6 mb-2">
                <div className="card card-inverse card-warning">
                  <div className="card-block bg-warning p-3">
                    <div className="rotate">
                      <i className="bi bi-currency-dollar fa-5x" />
                    </div>
                    <h6 className="text-uppercase">Revenue</h6>
                  
                  </div>
                </div>
              </div>
            </div>
            {/*/row*/}
            <hr />
            <div className="container">
              <div className="row my-3">
                <div className="col">
                  <h4>Chart Analytics</h4>
                </div>
              </div>
              <div className="row my-2">
                <div className="col-lg-6 py-1">
                  <div className="card">
                    <div className="card-body">
           
                    </div>
                  </div>
                </div>
                <div class="col-lg-6 py-1">
                      <div class="card">
                          <div class="card-body">
                        
                          </div>
                      </div>
                  </div>
              </div>
            </div>
            <a id="layouts" />
            <hr />
            <div className="row mb-3 container">
              <div className="col-lg-12" style={{ marginBottom: 100 }}>
                {/* Nav tabs */}
                <ul className="nav nav-tabs" role="tablist">
                  <li className="nav-item">
                    <a
                      className="nav-link active"
                      href="#home1"
                      role="tab"
                      data-toggle="tab"
                    >
                      Products
                    </a>
                  </li>
                  <li className="nav-item">
                    <a
                      className="nav-link"
                      href="#profile1"
                      role="tab"
                      data-toggle="tab"
                    >
                      Orders
                    </a>
                  </li>
                </ul>
                {/* Tab panes */}
                <div className="tab-content">
                  <br />
                  <div role="tabpanel" className="tab-pane active" id="home1">
                    <h4>Products</h4>
                
                  </div>
                  <div role="tabpanel" className="tab-pane" id="profile1">
                    <h4>Orders</h4>
               
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    </div>
    
      )
    }
    
    export default Dashboard