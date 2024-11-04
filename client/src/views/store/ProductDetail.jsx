import React, {useState, useEffect, useContext} from 'react'
import apiInstance from '../../utils/axioxs'
import { useParams } from 'react-router-dom'

import UserData from '../plugin/UserData'

import moment from "moment"



function ProductDetail() {
    const [product, setProduct] = useState([])
    const [specifications, setSpecifications] = useState([])
    const [gallery, setGallery] = useState([])
    const [color, SetColor] = useState([])
    const [size, setSize] = useState([])    

    const [colorValue, setColorValue] = useState("No Color")
    const [sizeValue, setSizeValue] = useState("No Size")  
    const [qtyValue, setQtyValue] = useState(1)

    const [review, setReviews]=useState([])
    const [createReview, setCreateReview] = useState({ user_id: 0, product_id: product?.id, review: "", rating: 0, })

   

    const param = useParams()
  

    
    useEffect(() => {
      apiInstance.get(`product/${param.slug}/`).then((res) => {
        setProduct(res.data)
        setSpecifications(res.data.specification)
        setGallery(res.data.gallery)
        SetColor(res.data.color)
        setSize(res.data.size)
      })
    }, [])  

    const handleColorButtoClick = (event) => {
      const colorNameInput =event.target.closest('.color_button').parentNode.querySelector(".color_name")
      setColorValue(colorNameInput.value)
    }

    const handleSizeButtonClick = (event) => {
        const sizeNameInput =event.target.closest('.size_button').parentNode.querySelector(".size_name")
        setSizeValue(sizeNameInput.value)
    }
    
    const handleQuantityChange = (event) => {
        setQtyValue(event.target.value)
    }

    const handleAddToCart = async () => {

        try {
            const formData = new FormData();

            formData.append('product_id', product.id);
      
            formData.append('qty', qtyValue);
            formData.append('price', product.price);
            formData.append('shipping_amount', product.shipping_amount);
       
            formData.append('color', colorValue);
            formData.append('size', sizeValue);
         
    
            // Make a post request to the cart api view
            const response = await apiInstance.post('cart-view/', formData);

            // Fetch update cart items
          
        
            

            
            
        
        } catch (error) {
            console.log(error);
        }
    }

   

    useEffect(() => {
       
    }, [console.log(product)])

    const handleReviewChange = (event) => {
        setCreateReview({
            ...createReview,
            [event.target.name]: event.target.value
        })
    }


    const handleReviewSubmit = (e) => {
        e.preventDefault()

        const formdata = new FormData()


        formdata.append('product_id', product?.id)
        formdata.append('rating', createReview.rating)
        formdata.append('review', createReview.review)

        
    }

    const handleAddToWishlist = async (productId, userId) => {
        try {
          const formData = new FormData();
          formData.append('product_id', productId);
          formData.append('user_id', userId);
          const response = await apiInstance.post(`customer/wishlist/${userId}/`, formData);
        
       
    
      } catch (error) {
          console.log(error);
      }
      };

      const fetchReviewsData =  () => {
        if (product !== null){
            apiInstance.get(`reviews/${product.id}/`).then((response) => {
                console.log(response.data)
                setReviews(response.data)
            })

          
        }
    }

    useEffect(() => {
        fetchReviewsData()
    },[product])

  return (
    <main className="mb-4 mt-4">
      <div className="container">
        {/* Section: Product details */}
        <section className="mb-9">
            <div className="row gx-lg-5">
                <div className="col-md-6 mb-4 mb-md-0">
                    {/* Gallery */}
                    <div className="">
                        <div className="row gx-2 gx-lg-3">
                            <div className="col-12 col-lg-12">
                                <div className="lightbox">
                                    <img
                                        src={product.image}
                                        style={{
                                            width: "100%",
                                            height: 500,
                                            objectFit: "cover",
                                            borderRadius: 10
                                        }}
                                        alt="Gallery image 1"
                                        className="ecommerce-gallery-main-img active w-100 rounded-4"
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="mt-3 d-flex">
                            {gallery.map((g, index) => (
                              <div className="p-3" key={index}>
                              <img
                                  src={g.image}
                                  style={{
                                      width: 100,
                                      height: 100,
                                      objectFit: "cover",
                                      borderRadius: 10
                                  }}
                                  alt="Gallery image 1"
                                  className="ecommerce-gallery-main-img active w-100 rounded-4"
                              />
                            </div>
                            ))}

                        </div>
                    </div>
                    {/* Gallery */}
                </div>
                <div className="col-md-6 mb-4 mb-md-0">
                    {/* Details */}
                    <div>
                        <h1 className="fw-bold mb-3">{product.title}</h1>
                        <div className="d-flex text-primary just align-items-center">
                            <ul className="mb-3 d-flex p-0" style={{ listStyle: "none" }}>
                                <li>
                                    <i className="fas fa-star fa-sm text-warning ps-0" title="Bad" />
                                    <i className="fas fa-star fa-sm text-warning ps-0" title="Bad" />
                                    <i className="fas fa-star fa-sm text-warning ps-0" title="Bad" />
                                    <i className="fas fa-star fa-sm text-warning ps-0" title="Bad" />
                                    <i className="fas fa-star fa-sm text-warning ps-0" title="Bad" />
                                </li>

                                <li style={{ marginLeft: 10, fontSize: 13 }}>
                                    <a href="" className="text-decoration-none">
                                        <strong className="me-2">{(Number(product?.product_rating)).toFixed(2)}</strong>({product?.rating_count} reviews)
                                    </a>
                                </li>
                            </ul>
                        </div>
                        <h5 className="mb-3">
                            <s className="text-muted me-2 small align-middle">${product.old_price}</s>
                            <span className="align-middle">${product.price}</span>
                        </h5>
                        <p className="text-muted">
                           {product.description}
                        </p>
                        <div className="table-responsive">
                            <table className="table table-sm table-borderless mb-0">
                                <tbody>
                                    <tr>
                                        <th className="ps-0 w-25" scope="row">
                                            <strong>Category</strong>
                                        </th>
                                        <td>{product.category?.title}</td>
                                    </tr>
                                    {specifications.map((s, index) => (
                                      <tr key={index}>
                                        <th className="ps-0 w-25" scope="row">
                                            <strong>{s.title}</strong>
                                        </th>
                                        <td>{s.content}</td>
                                      </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                        <hr className="my-5" />
                        <div>
                            <div className="row flex-column">
                                {/* Quantity */}
                                <div className="col-md-6 mb-4">
                                    <div className="form-outline">
                                        <label className="form-label" htmlFor="typeNumber"><b>Quantity</b></label>
                                        <input
                                            type="number"
                                            id="typeNumber"
                                            className="form-control quantity"
                                            min={1}
                                            value={qtyValue}
                                            onChange={handleQuantityChange}
                                        />
                                    </div>
                                </div>

                                {/* Size */}
                                    {size.length > 0 &&
                                    <>
                                    <div className="col-md-6 mb-4">
                                    <div className="form-outline">
                                        <label className="form-label" htmlFor="typeNumber"><b>Size: </b><span>{sizeValue}</span></label>
                                    </div>
                                    <div className='d-flex'>
                                    {size.map((s, index) => (
                                        <div key={index}>
                                            <input type="hidden" className='size_name' value={s.name}/>
                                            <button className='btn btn-secondary m-1 size_button' onClick={handleSizeButtonClick}>{s.name}</button>
                                        </div>
                                    ))}
                                    </div>
                                    </div>
                                </>
                                    
                                    }
                                
                                {/* Colors */}

                                {color.length > 0 &&
                                    <>
                                    <div className="col-md-6 mb-4">
                                    <div className="form-outline">
                                        <label className="form-label" htmlFor="typeNumber"><b>Color:</b> <span>{colorValue}</span></label>
                                    </div>
                                    <div className='d-flex'>
                                        {color.map((c, index) => (
                                          <div key={index}>
                                            <input type="hidden" className='color_name' value={c.name} />
                                            <button className='btn p-3 m-1 color_button' type='button' onClick={handleColorButtoClick} style={{ background: `${c.color_code}` }}></button>
                                          </div>
                                        ))}
                                        
                                    </div>
                                    <hr />
                                </div>
                                    </>
                                }

                            </div>
                            <button type="button" className="btn btn-primary btn-rounded me-2" onClick={handleAddToCart} title='Add to cart'>
                                <i className="fas fa-cart-plus me-2" /> Add to cart
                            </button>
                            <button onClick={() => handleAddToWishlist(product?.id)} href="#!" type="button" className="btn btn-danger btn-floating" data-mdb-toggle="tooltip" title="Add to wishlist">
                                <i className="fas fa-heart" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <hr />
        <ul className="nav nav-pills mb-3" id="pills-tab" role="tablist">
            <li className="nav-item" role="presentation">
                <button className="nav-link active" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">
                    Specifications
                </button>
            </li>
            <li className="nav-item" role="presentation">
                <button className="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">
                    Vendor
                </button>
            </li>
            <li className="nav-item" role="presentation">
                <button className="nav-link" id="pills-contact-tab" data-bs-toggle="pill" data-bs-target="#pills-contact" type="button" role="tab" aria-controls="pills-contact" aria-selected="false" >
                    Review
                </button>
            </li>
        </ul>
        <div className="tab-content" id="pills-tabContent">
            <div
                className="tab-pane fade show active"
                id="pills-home"
                role="tabpanel"
                aria-labelledby="pills-home-tab"
                tabIndex={0}
            >
                <div className="table-responsive">
                    <table className="table table-sm table-borderless mb-0">
                        <tbody>
                            <tr>
                                <th className="ps-0 w-25" scope="row">
                                    {" "}
                                    <strong>Category</strong>
                                </th>
                                <td>{product?.category?.title}</td>
                            </tr>

                            <tr>
                                <th className="ps-0 w-25" scope="row">
                                    {" "}
                                    <strong>Model</strong>
                                </th>
                                <td>{product?.title}</td>
                            </tr>

                            <tr>
                                <th className="ps-0 w-25" scope="row">
                                    {" "}
                                    <strong>Colors</strong>
                                </th>
                                <td>
                                {product?.color?.map((c, index) =>(
                                    <span>{c.name} </span>
                                ))}
                                </td>
                            </tr>
                            <tr>
                                <th className="ps-0 w-25" scope="row">
                                    {" "}
                                    <strong>Size</strong>
                                </th>
                                <td>
                                {product?.size?.map((s, index) =>(
                                    <span>{s.name} </span>
                                ))}
                                </td>
                            </tr>
                            <tr>
                                <th className="ps-0 w-25" scope="row">
                                    {" "}
                                    <strong>Delivery</strong>
                                </th>
                                <td>USA, Europe, Asians</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div
                className="tab-pane fade"
                id="pills-profile"
                role="tabpanel"
                aria-labelledby="pills-profile-tab"
                tabIndex={0}
            >
                <div className="card mb-3" style={{ maxWidth: 400 }}>
                    <div className="row g-0">
                        <div className="col-md-4">
                            <img
                                src={product?.vendor?.image}
                                style={{
                                    height: "100%",
                                    width: "100%",
                                    objectFit: "cover"
                                }}
                                alt="User Image"
                                className="img-fluid"
                            />
                        </div>
                        <div className="col-md-8">
                            <div className="card-body">
                                <h5 className="card-title">{product?.vendor?.name}</h5>
                                <p className="card-text">{product?.vendor?.description}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div
                className="tab-pane fade"
                id="pills-contact"
                role="tabpanel"
                aria-labelledby="pills-contact-tab"
                tabIndex={0}
            >
                <div className="container mt-5">
                    <div className="row">
                        {/* Column 1: Form to create a new review */}
                        <div className="col-md-6">
                            <h2>Create a New Review</h2>
                            <form onSubmit={handleReviewSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label">
                                        Rating
                                    </label>
                                    <select name="rating" className='form-select text-warning' onChange={handleReviewChange} id="">
                                        <option value="1">★</option>
                                        <option value="2">★★</option>
                                        <option value="3">★★★</option>
                                        <option value="4">★★★★</option>
                                        <option value="5">★★★★★</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="reviewText" className="form-label">
                                        Review
                                    </label>
                                    <textarea
                                        className="form-control"
                                        id="reviewText"
                                        rows={4}
                                        name='review'
                                        placeholder="Write your review"
                                        value={createReview.review}
                                        onChange={handleReviewChange}
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary">
                                    Submit Review
                                </button>
                            </form>
                        </div>
                        {/* Column 2: Display existing reviews */}
                        <div className="col-md-6">
                            <h2>Existing Reviews</h2>
                            {review?.map((r, index) => (
                                <div className="card mb-3" key={index}>
                                    <div className="row border g-0">
                                        <div className="col-md-3">
                                            <img
                                                src={r.profile.image}
                                                alt="User Image"
                                                className="img-fluid"
                                                style={{width:"100%", height:"100%", objectFit:"cover"}}
                                            />
                                        </div>
                                        <div className="col-md-9">
                                            <div className="card-body">
                                                <h5 className="card-title">{r.profile.full_name}</h5>
                                                <p className="card-text">{moment(r.date).format("MMM D, YYYY")}</p>
                                                <p className="card-text">
                                                    {r.review}<br />
                                                    {r.rating === 1 &&
                                                        <i className="fas fa-star fa-sm text-warning ps-0" />
                                                    }
                                                    {r.rating === 2 &&
                                                        <>
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                        </>
                                                    }
                                                    {r.rating === 3 &&
                                                        <>
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                        </>
                                                    }
                                                    {r.rating === 4 &&
                                                        <>
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                        </>
                                                    }
                                                    {r.rating === 5 &&
                                                        <>
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                            <i className="fas fa-star fa-sm text-warning ps-0" />
                                                        </>
                                                    }
                                                    
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {/* More reviews can be added here */}
                        </div>
                    </div>
                </div>
            </div>
            <div
                className="tab-pane fade"
                id="pills-disabled"
                role="tabpanel"
                aria-labelledby="pills-disabled-tab"
                tabIndex={0}
            >
                <div className="container mt-5">
                    <div className="row">
                        {/* Column 1: Form to submit new questions */}
                        <div className="col-md-6">
                            <h2>Ask a Question</h2>
                            <form>
                                <div className="mb-3">
                                    <label htmlFor="askerName" className="form-label">
                                        Your Name
                                    </label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="askerName"
                                        placeholder="Enter your name"
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="questionText" className="form-label">
                                        Question
                                    </label>
                                    <textarea
                                        className="form-control"
                                        id="questionText"
                                        rows={4}
                                        placeholder="Ask your question"
                                        defaultValue={""}
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary">
                                    Submit Question
                                </button>
                            </form>
                        </div>
                        {/* Column 2: Display existing questions and answers */}
                        <div className="col-md-6">
                            <h2>Questions and Answers</h2>
                            <div className="card mb-3">
                                <div className="card-body">
                                    <h5 className="card-title">User 1</h5>
                                    <p className="card-text">August 10, 2023</p>
                                    <p className="card-text">
                                        What are the available payment methods?
                                    </p>
                                    <h6 className="card-subtitle mb-2 text-muted">Answer:</h6>
                                    <p className="card-text">
                                        We accept credit/debit cards and PayPal as payment
                                        methods.
                                    </p>
                                </div>
                            </div>
                            <div className="card mb-3">
                                <div className="card-body">
                                    <h5 className="card-title">User 2</h5>
                                    <p className="card-text">August 15, 2023</p>
                                    <p className="card-text">How long does shipping take?</p>
                                    <h6 className="card-subtitle mb-2 text-muted">Answer:</h6>
                                    <p className="card-text">
                                        Shipping usually takes 3-5 business days within the US.
                                    </p>
                                </div>
                            </div>
                            {/* More questions and answers can be added here */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </main>
  )
}

export default ProductDetail