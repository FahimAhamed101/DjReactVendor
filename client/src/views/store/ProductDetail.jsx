import { useState, useEffect, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import moment from "moment";

import apiInstance from "../../utils/axios";
import GetCurrentAddress from "../plugin/UserCountry";
import UserData from "../plugin/UserData";
import CartID from "../plugin/CartID";
import { CartContext } from "../plugin/Context";

import { Toast, AlertFailed } from "../base/Alert";

function ProductDetail() {
  const [product, setProduct] = useState({});
  const [specifications, setSpecifications] = useState([]);
  const [gallery, setGallery] = useState([]);
  const [selectedImage, setSelectedImage] = useState("");
  const [selectedSize, setSelectedSize] = useState("");
  const [selectedColor, setSelectedColor] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [activeTab, setActiveTab] = useState("specifications");
  const [question, setQuestion] = useState({ name: "", content: "" });

  const [cartCount, setCartCount] = useContext(CartContext);

  const [reviews, setReviews] = useState([]);
  const [createReview, setCreateReview] = useState({
    user_id: 0,
    product_id: 0,
    review: "",
    rating: 5,
  });

  const param = useParams();
  const currentAddress = GetCurrentAddress();
  const userData = UserData();
  const cart_id = CartID();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await apiInstance.get(`products/${param.slug}/`);
        const productData = response.data;
        setProduct(productData);
        setSpecifications(productData.specification || []);
        setGallery(productData.gallery || []);
        setSelectedImage(productData.image);
        setSelectedSize(productData.size?.[0]?.name || "");
        setSelectedColor(productData.color?.[0]?.name || "");
        
        // Update createReview with the product ID
        setCreateReview(prev => ({
          ...prev,
          product_id: productData.id
        }));
      } catch (error) {
        console.error("Error fetching product:", error);
      }
    };

    fetchProduct();
  }, [param.slug]);

  const handleImageSelect = (image) => {
    setSelectedImage(image);
  };

  const handleAddToCart = async () => {
    try {
      if (!product.id) {
        throw new Error("Product information not loaded yet");
      }

      const formData = new FormData();
      formData.append("product_id", product.id);
      formData.append("user_id", userData?.user_id || 0);
      formData.append("qty", quantity);
      formData.append("price", product.price);
      formData.append("shipping_amount", product.shipping_amount);
      formData.append("country", currentAddress.country);
      formData.append("size", selectedSize);
      formData.append("color", selectedColor);
      formData.append("cart_id", cart_id);

      const response = await apiInstance.post("cart-view/", formData);

      const url = userData
        ? `cart-list/${cart_id}/${userData?.user_id}/`
        : `cart-list/${cart_id}/`;

      const cartResponse = await apiInstance.get(url);
      setCartCount(cartResponse.data.length);

      Toast.fire({
        icon: "success",
        title: response.data.message || "Product added to cart",
      });
    } catch (error) {
      console.error("Error adding to cart:", error);
      AlertFailed.fire({
        icon: "error",
        title: error.response?.data?.message || "Failed to add to cart",
      });
    }
  };

  const fetchReviewData = async () => {
    if (product?.id) {
      try {
        const response = await apiInstance.get(`reviews/${product.id}/`);
        setReviews(response.data);
      } catch (error) {
        console.error("Error fetching reviews:", error);
      }
    }
  };

  useEffect(() => {
    fetchReviewData();
  }, [product]);

  const handleReviewChange = (event) => {
    const { name, value } = event.target;
    setCreateReview({
      ...createReview,
      [name]: name === "rating" ? parseInt(value) : value,
    });
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    if (!createReview.review.trim()) {
      AlertFailed.fire({
        icon: "error",
        title: "Please write a review",
      });
      return;
    }

    try {
      const formData = new FormData();
      formData.append("user_id", userData?.user_id || 0);
      formData.append("product_id", product.id);
      formData.append("rating", createReview.rating);
      formData.append("review", createReview.review);

      await apiInstance.post(`reviews/${product.id}/`, formData);
      
      // Refresh reviews
      await fetchReviewData();
      
      // Reset form
      setCreateReview({
        ...createReview,
        review: "",
        rating: 5
      });

      Toast.fire({
        icon: "success",
        title: "Review submitted successfully",
      });
    } catch (error) {
      console.error("Error submitting review:", error);
      AlertFailed.fire({
        icon: "error",
        title: error.response?.data?.message || "Failed to submit review",
      });
    }
  };

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    
    if (!question.name.trim() || !question.content.trim()) {
      AlertFailed.fire({
        icon: "error",
        title: "Please fill all fields",
      });
      return;
    }

    try {
      // Here you would typically send the question to your backend
      // For now, we'll just show a success message
      Toast.fire({
        icon: "success",
        title: "Question submitted successfully",
      });
      
      // Reset form
      setQuestion({ name: "", content: "" });
    } catch (error) {
      console.error("Error submitting question:", error);
      AlertFailed.fire({
        icon: "error",
        title: "Failed to submit question",
      });
    }
  };

  return (
    <div className="container py-4">
      <div className="row g-4">
        {/* Product Images Section */}
        <div className="col-lg-5">
          <div
            className="position-relative rounded-3 overflow-hidden mb-3"
            style={{
              minHeight: "400px",
              transition: "all 0.3s ease",
            }}
          >
            <img
              src={selectedImage}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                position: "absolute",
                top: "0",
                left: "0",
                WebkitUserSelect: "none",
              }}
              alt={product.title}
            />
          </div>
          <div className="row g-2">
            <div
              className="col-3 cursor-pointer"
              onClick={() => handleImageSelect(product.image)}
            >
              <div className="ratio ratio-1x1 rounded-1 overflow-hidden">
                <img
                  src={product.image}
                  style={{ objectFit: "cover", width: "100%", height: "100%" }}
                  alt="Main"
                />
              </div>
            </div>
            {gallery.map((item, index) => (
              <div
                key={index}
                className="col-3 cursor-pointer"
                onClick={() => handleImageSelect(item.image)}
              >
                <div className="ratio ratio-1x1 rounded-1 overflow-hidden">
                  <img
                    src={item.image}
                    style={{
                      objectFit: "cover",
                      width: "100%",
                      height: "100%",
                    }}
                    alt={`Gallery ${index + 1}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Product Info Section */}
        <div className="col-lg-6">
          <div className="ps-lg-4">
            <nav aria-label="breadcrumb">
              <ol className="breadcrumb mb-2">
                <li className="breadcrumb-item">
                  <Link
                    to={"/"}
                    className="text-decoration-none text-muted small"
                  >
                    Home
                  </Link>
                </li>
                <li className="breadcrumb-item">
                  <Link
                    to={`/category/${product.category?.slug}`}
                    className="text-decoration-none text-muted small"
                  >
                    {product.category?.title}
                  </Link>
                </li>
                <li className="breadcrumb-item text-muted" aria-current="page">
                  {product.title}
                </li>
              </ol>
            </nav>

            <h1
              style={{ fontSize: "1.75rem", fontWeight: "600" }}
              className="mb-2"
            >
              {product.title}
            </h1>

            <div className="d-flex align-items-center mb-2">
              <div className="text-warning me-2" style={{ fontSize: "0.9rem" }}>
                {"★".repeat(Math.round(product.product_rating || 0))}
                {"☆".repeat(5 - Math.round(product.product_rating || 0))}
              </div>
              <span className="text-muted small">
                ({product.rating_count || 0} reviews)
              </span>
            </div>

            <div className="mb-3">
              <span className="h4 text-primary me-2">${product.price}</span>
              {product.old_price && (
                <del className="text-muted small">${product.old_price}</del>
              )}
            </div>

            <p className="text-muted small mb-4">{product.description}</p>

            {product.size?.length > 0 && (
              <div className="mb-4">
                <h6 className="mb-2 small fw-bold">Size: {selectedSize}</h6>
                <div className="d-flex gap-2">
                  {product.size.map((size, index) => (
                    <button
                      key={index}
                      className={`btn btn-sm ${
                        selectedSize === size.name
                          ? "btn-warning"
                          : "btn-outline-secondary"
                      }`}
                      style={{ WebkitTransition: "all 0.2s ease" }}
                      onClick={() => setSelectedSize(size.name)}
                    >
                      {size.name}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {product.color?.length > 0 && (
              <div className="mb-4">
                <h6 className="mb-2 small fw-bold">Color: {selectedColor}</h6>
                <div className="d-flex gap-2">
                  {product.color.map((color, index) => (
                    <button
                      key={index}
                      className={`btn rounded-circle p-3 border ${
                        selectedColor === color.name
                          ? "border-warning border-3"
                          : ""
                      }`}
                      style={{
                        width: "30px",
                        height: "30px",
                        backgroundColor: color.color_code,
                        WebkitTransition: "all 0.2s ease",
                      }}
                      onClick={() => setSelectedColor(color.name)}
                      title={color.name}
                    />
                  ))}
                </div>
              </div>
            )}

            <div className="mb-4">
              <h6 className="mb-2 small fw-bold">Quantity</h6>
              <div
                className="input-group input-group-sm"
                style={{ maxWidth: "150px" }}
              >
                <button
                  className="btn btn-outline-secondary"
                  onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                >
                  −
                </button>
                <input
                  type="number"
                  className="form-control text-center"
                  value={quantity}
                  onChange={(e) =>
                    setQuantity(Math.max(1, parseInt(e.target.value) || 1))
                  }
                  style={{ WebkitAppearance: "none" }}
                />
                <button
                  className="btn btn-outline-secondary"
                  onClick={() => setQuantity((q) => q + 1)}
                >
                  +
                </button>
              </div>
            </div>

            <div className="d-flex gap-2 mb-4">
              <button
                className="btn btn-warning btn-lg"
                onClick={handleAddToCart}
                style={{
                  flex: "1",
                  WebkitTransition: "all 0.2s ease",
                }}
              >
                <i className="fas fa-shopping-cart me-2"></i>
                Add to Cart
              </button>
              <button
                className="btn btn-dark"
                style={{ WebkitTransition: "all 0.2s ease" }}
              >
                <i className="fas fa-heart"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <br></br>

      {/* Tabs Section */}
      <div className="row mt-5">
        <div className="col-12">
          <ul
            className="nav nav-tabs nav-fill flex-column flex-md-row"
            role="tablist"
            style={{ borderBottom: "1px solid #dee2e6" }}
          >
            {["specifications", "vendor", "reviews", "faq"].map((tab) => (
              <li className="nav-item" key={tab}>
                <button
                  className={`nav-link text-capitalize ${
                    activeTab === tab ? "active" : ""
                  }`}
                  onClick={() => setActiveTab(tab)}
                  style={{
                    border: "none",
                    borderBottom:
                      activeTab === tab ? "2px solid #D57907" : "none",
                    borderRadius: "0",
                    padding: "1rem",
                    color: activeTab === tab ? "#000000" : "#6c757d",
                    fontWeight: "500",
                    WebkitTransition: "all 0.2s ease",
                  }}
                >
                  {tab}
                </button>
              </li>
            ))}
          </ul>

          <div className="tab-content py-4">
            {activeTab === "specifications" && (
              <div className="row">
                <div className="col-md-8">
                  <table className="table table-striped">
                    <tbody>
                      {specifications.map((spec, index) => (
                        <tr key={index}>
                          <th className="w-25 small">{spec.title}</th>
                          <td className="small">{spec.content}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {activeTab === "vendor" && product.vendor && (
              <div className="row justify-content-center">
                <div className="col-md-8">
                  <div className="card border-0.5 text-center border-light">
                    <div className="card-body p-4">
                      <div
                        className="rounded-circle overflow-hidden mx-auto mb-3"
                        style={{ width: "120px", height: "120px" }}
                      >
                        <img
                          src={product.vendor.image}
                          style={{
                            width: "100%",
                            height: "100%",
                            objectFit: "cover",
                          }}
                          alt={product.vendor.name}
                        />
                      </div>
                      <h5 className="mb-2">{product.vendor.name}</h5>
                      <p className="text-muted small mb-3">
                        {product.vendor.description}
                      </p>
                      <div className="d-flex justify-content-center gap-2">
                        <button className="btn btn-warning">Follow</button>
                        <button className="btn btn-dark">Message</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "reviews" && (
              <div className="row">
                <div className="col-md-6 mb-4">
                  <div className="card border-0.5 border-light">
                    <div className="card-body p-4">
                      <h5 className="mb-3">Write a Review</h5>
                      <div className="mb-3">
                        <label className="form-label small">Rating</label>
                        <select
                          className="form-select form-select-sm"
                          name="rating"
                          value={createReview.rating}
                          onChange={handleReviewChange}
                        >
                          <option value="1">1 Star</option>
                          <option value="2">2 Star</option>
                          <option value="3">3 Star</option>
                          <option value="4">4 Star</option>
                          <option value="5">5 Star</option>
                        </select>
                      </div>
                      <div className="mb-3">
                        <label className="form-label small">Your Review</label>
                        <textarea
                          className="form-control form-control-sm"
                          rows="3"
                          required
                          name="review"
                          value={createReview.review}
                          onChange={handleReviewChange}
                          placeholder="Share your experience..."
                        ></textarea>
                      </div>
                      <button
                        type="submit"
                        onClick={handleReviewSubmit}
                        className="btn btn-warning btn-sm"
                        disabled={!createReview.review.trim()}
                      >
                        Submit Review
                      </button>
                    </div>
                  </div>
                </div>
                <div className="col-md-6">
                  {reviews.length > 0 ? (
                    <div className="d-flex flex-column gap-3">
                      {reviews
                        .sort((a, b) => new Date(b.date) - new Date(a.date))
                        .map((r, index) => (
                          <div
                            key={index}
                            className="card border-0.5 border-light"
                          >
                            <div className="card-body p-3">
                              <div className="d-flex align-items-center mb-2">
                                <img
                                  src={r.profile?.image}
                                  className="rounded-circle me-2"
                                  alt="User"
                                  style={{
                                    width: "40px",
                                    height: "40px",
                                    objectFit: "cover",
                                  }}
                                />
                                <div>
                                  <h6 className="mb-0 small">
                                    {r.profile?.full_name}
                                  </h6>
                                  <div
                                    className="text-warning"
                                    style={{ fontSize: "0.8rem" }}
                                  >
                                    {"★".repeat(r.rating)}
                                  </div>
                                </div>
                                <small className="text-muted ms-auto">
                                  {moment(r.date).format(
                                    "dddd, D MMMM, YYYY, h:mm A"
                                  )}
                                </small>
                              </div>
                              <p className="small mb-0">{r.review}</p>
                            </div>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <div className="alert alert-info">
                      No reviews yet. Be the first to review!
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === "faq" && (
              <div className="row">
                <div className="col-md-6 mb-4">
                  <div className="card border-0.5 border-light">
                    <div className="card-body p-4">
                      <h5 className="mb-3">Ask a Question</h5>
                      <div className="mb-3">
                        <label className="form-label small">Your Name</label>
                        <input
                          type="text"
                          className="form-control form-control-sm"
                          value={question.name}
                          onChange={(e) =>
                            setQuestion({ ...question, name: e.target.value })
                          }
                          placeholder="Enter your name"
                        />
                      </div>
                      <div className="mb-3">
                        <label className="form-label small">
                          Your Question
                        </label>
                        <textarea
                          className="form-control form-control-sm"
                          rows="3"
                          value={question.content}
                          onChange={(e) =>
                            setQuestion({
                              ...question,
                              content: e.target.value,
                            })
                          }
                          placeholder="What would you like to know?"
                        ></textarea>
                      </div>
                      <button 
                        className="btn btn-warning btn-sm"
                        onClick={handleQuestionSubmit}
                        disabled={!question.name.trim() || !question.content.trim()}
                      >
                        Submit Question
                      </button>
                    </div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="d-flex flex-column gap-3">
                    {[1, 2].map((_, index) => (
                      <div key={index} className="card border-0.5 border-light">
                        <div className="card-body p-3">
                          <div className="d-flex align-items-center mb-2">
                            <img
                              src="https://placehold.co/600x400"
                              className="rounded-circle me-2"
                              alt="User"
                              style={{
                                width: "40px",
                                height: "40px",
                                objectFit: "cover",
                              }}
                            />
                            <div>
                              <h6 className="mb-0 small">Jane Smith</h6>
                              <small className="text-muted">
                                Asked on Jan 15, 2024
                              </small>
                            </div>
                          </div>
                          <p className="small mb-3">
                            What&apos;s the battery life like on this laptop?
                          </p>
                          <div className="border-start border-dark ps-3">
                            <p className="small mb-1 text-warning">
                              Answer from Vendor:
                            </p>
                            <p className="small mb-0">
                              The battery life typically lasts between 6-8 hours
                              with normal usage. This can vary depending on your
                              settings and usage patterns.
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;