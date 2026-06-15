import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import json

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MallQ! - Mall Companion",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-bg: #0f0f23;
        --secondary-bg: #1a1a2e;
        --card-bg: #16213e;
        --accent-purple: #7c3aed;
        --accent-blue: #3b82f6;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --success-green: #22c55e;
        --warning-orange: #f97316;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid #2d2d44;
    }
    
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    
    .app-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Stat cards */
    .stat-card {
        background: #1a1a2e;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2d2d44;
        text-align: center;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .stat-subtext {
        font-size: 0.8rem;
        color: #22c55e;
        margin-top: 0.25rem;
    }
    
    /* Product cards */
    .product-card {
        background: #1a1a2e;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #2d2d44;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1rem;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.15);
    }
    
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .product-info {
        padding: 1rem;
    }
    
    .product-name {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.25rem;
    }
    
    .product-brand {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 0.5rem;
    }
    
    .product-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: #22c55e;
    }
    
    .product-original-price {
        font-size: 0.9rem;
        color: #94a3b8;
        text-decoration: line-through;
        margin-left: 0.5rem;
    }
    
    /* Store cards */
    .store-card {
        background: linear-gradient(180deg, rgba(26, 26, 46, 0.8) 0%, #1a1a2e 100%);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #2d2d44;
        position: relative;
    }
    
    .store-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.7);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        color: white;
    }
    
    .store-rating {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(0, 0, 0, 0.5);
        padding: 4px 8px;
        border-radius: 8px;
        font-size: 0.85rem;
    }
    
    /* Category pills */
    .category-pill {
        display: inline-block;
        padding: 6px 14px;
        background: #2d2d44;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #ffffff;
        margin-right: 8px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .category-pill:hover, .category-pill.active {
        background: #7c3aed;
    }
    
    /* Alert badge */
    .alert-badge {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #7c3aed;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    /* Search section */
    .search-section {
        background: #1a1a2e;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #2d2d44;
        margin-bottom: 1.5rem;
    }
    
    /* Promo card */
    .promo-card {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .promo-code {
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 8px;
        font-family: monospace;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: #1a1a2e;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2d2d44;
        height: 100%;
    }
    
    .dashboard-title {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    /* Query bar */
    .query-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        background: #0f0f23;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .query-text {
        color: #ffffff;
        font-size: 0.9rem;
    }
    
    .query-count {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    /* Progress bar */
    .progress-container {
        background: #0f0f23;
        border-radius: 4px;
        height: 6px;
        margin-top: 4px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #7c3aed, #3b82f6);
        border-radius: 4px;
    }
    
    /* Segment distribution */
    .segment-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #2d2d44;
    }
    
    .segment-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    /* Inventory table */
    .inventory-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: #0f0f23;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border: 1px solid #2d2d44;
    }
    
    .inventory-image {
        width: 60px;
        height: 60px;
        border-radius: 8px;
        object-fit: cover;
    }
    
    /* Size badges */
    .size-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 32px;
        background: #2d2d44;
        border-radius: 6px;
        font-size: 0.8rem;
        color: white;
        margin-right: 4px;
    }
    
    .size-count {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-left: 2px;
    }
    
    /* Coupon card merchant */
    .coupon-active {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    /* Navigation tabs */
    .nav-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .nav-tab {
        padding: 0.75rem 1.5rem;
        background: #1a1a2e;
        border: 1px solid #2d2d44;
        border-radius: 10px;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .nav-tab:hover, .nav-tab.active {
        background: #7c3aed;
        color: white;
        border-color: #7c3aed;
    }
    
    /* Live alerts */
    .live-alert {
        background: #1a1a2e;
        border-left: 4px solid #f97316;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2d2d44;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #7c3aed;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.5rem;
        }
        .stat-value {
            font-size: 1.4rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA INITIALIZATION
# ============================================

@st.cache_data
def load_mall_data():
    """Load comprehensive mall data with real brands, products, and pricing"""
    
    # Store information
    stores = {
        "ZARA": {
            "id": "zara",
            "name": "ZARA",
            "category": "Fashion",
            "level": "First",
            "rating": 4.6,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Zara_Logo.svg",
            "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
            "description": "Spanish fashion retailer known for trendy clothing"
        },
        "H&M": {
            "id": "hm",
            "name": "H&M",
            "category": "Fashion",
            "level": "Ground",
            "rating": 4.5,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg",
            "image": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=400",
            "description": "Swedish multinational clothing company"
        },
        "Nike": {
            "id": "nike",
            "name": "Nike",
            "category": "Footwear",
            "level": "First",
            "rating": 4.8,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg",
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "description": "World's largest athletic footwear and apparel company"
        },
        "Adidas": {
            "id": "adidas",
            "name": "Adidas Outlet",
            "store_key": "Adidas",
            "category": "Footwear",
            "level": "Ground",
            "rating": 4.7,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg",
            "image": "https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=400",
            "description": "German athletic and casual footwear brand"
        },
        "Levi's": {
            "id": "levis",
            "name": "Levi's",
            "category": "Fashion",
            "level": "First",
            "rating": 4.5,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/7/75/Levi%27s_logo.svg",
            "image": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=400",
            "description": "Iconic American denim jeans brand"
        },
        "Apple": {
            "id": "apple",
            "name": "Apple Store",
            "store_key": "Apple",
            "category": "Electronics",
            "level": "Ground",
            "rating": 4.9,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
            "image": "https://images.unsplash.com/photo-1491933382434-500287f9b54b?w=400",
            "description": "Premium electronics and accessories"
        },
        "Fossil": {
            "id": "fossil",
            "name": "Fossil",
            "category": "Accessories",
            "level": "Second",
            "rating": 4.4,
            "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Fossil_Group_logo.svg",
            "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400",
            "description": "American fashion designer and manufacturer of watches"
        },
        "Hamleys": {
            "id": "hamleys",
            "name": "Hamleys",
            "category": "Toys",
            "level": "Second",
            "rating": 4.6,
            "logo": "https://upload.wikimedia.org/wikipedia/en/7/74/Hamleys_Logo.svg",
            "image": "https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400",
            "description": "World-famous toy store since 1760"
        }
    }
    
    # Product catalog with real prices in INR
    products = [
        # ZARA Products
        {
            "id": "p001",
            "name": "White Relaxed Fit Cotton Shirt",
            "brand": "ZARA",
            "store": "ZARA",
            "category": "Shirts",
            "subcategory": "Casual Shirts",
            "price": 2990,
            "original_price": 3990,
            "discount": 25,
            "color": "White",
            "sizes": {"S": 5, "M": 8, "L": 12, "XL": 6},
            "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
            "rating": 4.5,
            "reviews": 128
        },
        {
            "id": "p002",
            "name": "Oversized Graphic Print Tee",
            "brand": "ZARA",
            "store": "ZARA",
            "category": "T-Shirts",
            "subcategory": "Graphic Tees",
            "price": 1590,
            "original_price": 1990,
            "discount": 20,
            "color": "Black",
            "sizes": {"S": 10, "M": 15, "L": 20, "XL": 8},
            "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400",
            "rating": 4.3,
            "reviews": 95
        },
        {
            "id": "p003",
            "name": "Slim Fit Chino Pants",
            "brand": "ZARA",
            "store": "ZARA",
            "category": "Pants",
            "subcategory": "Chinos",
            "price": 2490,
            "original_price": 2990,
            "discount": 17,
            "color": "Beige",
            "sizes": {"30": 6, "32": 10, "34": 8, "36": 4},
            "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
            "rating": 4.4,
            "reviews": 76
        },
        
        # H&M Products
        {
            "id": "p004",
            "name": "Regular Fit Oxford Shirt",
            "brand": "H&M",
            "store": "H&M",
            "category": "Shirts",
            "subcategory": "Formal Shirts",
            "price": 1499,
            "original_price": 1999,
            "discount": 25,
            "color": "Light Blue",
            "sizes": {"S": 12, "M": 18, "L": 15, "XL": 10},
            "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400",
            "rating": 4.2,
            "reviews": 203
        },
        {
            "id": "p005",
            "name": "Basic Cotton T-Shirt Pack",
            "brand": "H&M",
            "store": "H&M",
            "category": "T-Shirts",
            "subcategory": "Basic Tees",
            "price": 999,
            "original_price": 1299,
            "discount": 23,
            "color": "Multi",
            "sizes": {"S": 25, "M": 30, "L": 28, "XL": 20},
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            "rating": 4.6,
            "reviews": 456
        },
        {
            "id": "p006",
            "name": "Skinny Fit Jeans",
            "brand": "H&M",
            "store": "H&M",
            "category": "Jeans",
            "subcategory": "Skinny Jeans",
            "price": 1999,
            "original_price": 2499,
            "discount": 20,
            "color": "Dark Blue",
            "sizes": {"28": 8, "30": 12, "32": 15, "34": 10},
            "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
            "rating": 4.3,
            "reviews": 312
        },
        
        # Nike Products
        {
            "id": "p007",
            "name": "Air Max 270 React",
            "brand": "Nike",
            "store": "Nike",
            "category": "Shoes",
            "subcategory": "Running Shoes",
            "price": 12995,
            "original_price": 15995,
            "discount": 19,
            "color": "White/Black",
            "sizes": {"UK7": 5, "UK8": 8, "UK9": 10, "UK10": 6},
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "rating": 4.8,
            "reviews": 567
        },
        {
            "id": "p008",
            "name": "Court Vision Low",
            "brand": "Nike",
            "store": "Nike",
            "category": "Shoes",
            "subcategory": "Casual Sneakers",
            "price": 4995,
            "original_price": 5995,
            "discount": 17,
            "color": "White",
            "sizes": {"UK7": 12, "UK8": 15, "UK9": 18, "UK10": 10},
            "image": "https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=400",
            "rating": 4.6,
            "reviews": 892
        },
        {
            "id": "p009",
            "name": "Dri-FIT Running T-Shirt",
            "brand": "Nike",
            "store": "Nike",
            "category": "T-Shirts",
            "subcategory": "Sports Tees",
            "price": 1995,
            "original_price": 2495,
            "discount": 20,
            "color": "Grey",
            "sizes": {"S": 20, "M": 25, "L": 22, "XL": 15},
            "image": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400",
            "rating": 4.7,
            "reviews": 234
        },
        
        # Adidas Products
        {
            "id": "p010",
            "name": "Ultraboost 22",
            "brand": "Adidas",
            "store": "Adidas",
            "category": "Shoes",
            "subcategory": "Running Shoes",
            "price": 14999,
            "original_price": 18999,
            "discount": 21,
            "color": "Core Black",
            "sizes": {"UK7": 4, "UK8": 6, "UK9": 8, "UK10": 5},
            "image": "https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=400",
            "rating": 4.9,
            "reviews": 723
        },
        {
            "id": "p011",
            "name": "Stan Smith Classic",
            "brand": "Adidas",
            "store": "Adidas",
            "category": "Shoes",
            "subcategory": "Casual Sneakers",
            "price": 6999,
            "original_price": 8999,
            "discount": 22,
            "color": "White/Green",
            "sizes": {"UK7": 10, "UK8": 14, "UK9": 12, "UK10": 8},
            "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400",
            "rating": 4.7,
            "reviews": 1045
        },
        {
            "id": "p012",
            "name": "Essentials 3-Stripes Pants",
            "brand": "Adidas",
            "store": "Adidas",
            "category": "Pants",
            "subcategory": "Track Pants",
            "price": 2999,
            "original_price": 3999,
            "discount": 25,
            "color": "Black",
            "sizes": {"S": 15, "M": 20, "L": 18, "XL": 12},
            "image": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400",
            "rating": 4.5,
            "reviews": 456
        },
        
        # Levi's Products
        {
            "id": "p013",
            "name": "501 Original Fit Jeans",
            "brand": "Levi's",
            "store": "Levi's",
            "category": "Jeans",
            "subcategory": "Straight Fit",
            "price": 4999,
            "original_price": 6499,
            "discount": 23,
            "color": "Medium Indigo",
            "sizes": {"30": 8, "32": 12, "34": 15, "36": 10},
            "image": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=400",
            "rating": 4.8,
            "reviews": 1567
        },
        {
            "id": "p014",
            "name": "511 Slim Fit Jeans",
            "brand": "Levi's",
            "store": "Levi's",
            "category": "Jeans",
            "subcategory": "Slim Fit",
            "price": 3999,
            "original_price": 5299,
            "discount": 25,
            "color": "Dark Blue",
            "sizes": {"28": 6, "30": 10, "32": 14, "34": 12},
            "image": "https://images.unsplash.com/photo-1604176354204-9268737828e4?w=400",
            "rating": 4.7,
            "reviews": 987
        },
        {
            "id": "p015",
            "name": "Classic Western Denim Shirt",
            "brand": "Levi's",
            "store": "Levi's",
            "category": "Shirts",
            "subcategory": "Denim Shirts",
            "price": 3499,
            "original_price": 4499,
            "discount": 22,
            "color": "Light Wash",
            "sizes": {"S": 5, "M": 8, "L": 10, "XL": 6},
            "image": "https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=400",
            "rating": 4.4,
            "reviews": 234
        },
        
        # Fossil Products (Watches)
        {
            "id": "p016",
            "name": "Neutra Chronograph Watch",
            "brand": "Fossil",
            "store": "Fossil",
            "category": "Watches",
            "subcategory": "Chronograph",
            "price": 9995,
            "original_price": 12995,
            "discount": 23,
            "color": "Silver/Blue",
            "sizes": {"One Size": 15},
            "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400",
            "rating": 4.6,
            "reviews": 345
        },
        {
            "id": "p017",
            "name": "Gen 6 Smartwatch",
            "brand": "Fossil",
            "store": "Fossil",
            "category": "Watches",
            "subcategory": "Smartwatch",
            "price": 22995,
            "original_price": 28995,
            "discount": 21,
            "color": "Black",
            "sizes": {"One Size": 8},
            "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400",
            "rating": 4.5,
            "reviews": 567
        },
        {
            "id": "p018",
            "name": "Minimalist Leather Watch",
            "brand": "Fossil",
            "store": "Fossil",
            "category": "Watches",
            "subcategory": "Analog",
            "price": 7495,
            "original_price": 9495,
            "discount": 21,
            "color": "Brown/White",
            "sizes": {"One Size": 20},
            "image": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=400",
            "rating": 4.7,
            "reviews": 423
        },
        
        # Hamleys Products (Toys)
        {
            "id": "p019",
            "name": "LEGO Technic Supercar",
            "brand": "LEGO",
            "store": "Hamleys",
            "category": "Toys",
            "subcategory": "Building Sets",
            "price": 14999,
            "original_price": 17999,
            "discount": 17,
            "color": "Multi",
            "sizes": {"One Size": 5},
            "image": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400",
            "rating": 4.9,
            "reviews": 234
        },
        {
            "id": "p020",
            "name": "Remote Control Racing Car",
            "brand": "Hot Wheels",
            "store": "Hamleys",
            "category": "Toys",
            "subcategory": "RC Vehicles",
            "price": 2999,
            "original_price": 3999,
            "discount": 25,
            "color": "Red",
            "sizes": {"One Size": 12},
            "image": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400",
            "rating": 4.4,
            "reviews": 189
        },
        {
            "id": "p021",
            "name": "Barbie Dreamhouse",
            "brand": "Barbie",
            "store": "Hamleys",
            "category": "Toys",
            "subcategory": "Dolls",
            "price": 8999,
            "original_price": 11999,
            "discount": 25,
            "color": "Pink",
            "sizes": {"One Size": 8},
            "image": "https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400",
            "rating": 4.7,
            "reviews": 345
        },
        
        # Apple Products
        {
            "id": "p022",
            "name": "Apple Watch Series 9",
            "brand": "Apple",
            "store": "Apple",
            "category": "Watches",
            "subcategory": "Smartwatch",
            "price": 41900,
            "original_price": 44900,
            "discount": 7,
            "color": "Midnight",
            "sizes": {"41mm": 6, "45mm": 8},
            "image": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400",
            "rating": 4.9,
            "reviews": 2345
        },
        {
            "id": "p023",
            "name": "AirPods Pro 2nd Gen",
            "brand": "Apple",
            "store": "Apple",
            "category": "Electronics",
            "subcategory": "Audio",
            "price": 24900,
            "original_price": 26900,
            "discount": 7,
            "color": "White",
            "sizes": {"One Size": 25},
            "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400",
            "rating": 4.8,
            "reviews": 3456
        },
        
        # More variety products
        {
            "id": "p024",
            "name": "Premium Polo T-Shirt",
            "brand": "ZARA",
            "store": "ZARA",
            "category": "T-Shirts",
            "subcategory": "Polo",
            "price": 2290,
            "original_price": 2990,
            "discount": 23,
            "color": "Navy Blue",
            "sizes": {"S": 8, "M": 12, "L": 10, "XL": 6},
            "image": "https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=400",
            "rating": 4.4,
            "reviews": 156
        },
        {
            "id": "p025",
            "name": "Air Force 1 '07",
            "brand": "Nike",
            "store": "Nike",
            "category": "Shoes",
            "subcategory": "Casual Sneakers",
            "price": 7495,
            "original_price": 8995,
            "discount": 17,
            "color": "White",
            "sizes": {"UK7": 8, "UK8": 12, "UK9": 15, "UK10": 10},
            "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400",
            "rating": 4.9,
            "reviews": 2134
        },
    ]
    
    # Active promotional coupons
    coupons = [
        {
            "id": "c001",
            "store": "ZARA",
            "title": "End of Season Sale",
            "code": "ZARA30",
            "discount": 30,
            "valid_until": "2026-06-30",
            "min_purchase": 2000
        },
        {
            "id": "c002",
            "store": "H&M",
            "title": "Circular Recycle Promo",
            "code": "HMRECYCLE15",
            "discount": 15,
            "valid_until": "2026-07-15",
            "min_purchase": 1500
        },
        {
            "id": "c003",
            "store": "Nike",
            "title": "Member Exclusive",
            "code": "NIKEMEMBER20",
            "discount": 20,
            "valid_until": "2026-06-25",
            "min_purchase": 5000
        },
        {
            "id": "c004",
            "store": "Adidas",
            "title": "Summer Sports Festival",
            "code": "ADISUMMER25",
            "discount": 25,
            "valid_until": "2026-07-01",
            "min_purchase": 4000
        },
        {
            "id": "c005",
            "store": "Levi's",
            "title": "Denim Days",
            "code": "LEVIS501",
            "discount": 20,
            "valid_until": "2026-06-28",
            "min_purchase": 3000
        },
        {
            "id": "c006",
            "store": "Fossil",
            "title": "Watch Fest",
            "code": "FOSSIL15OFF",
            "discount": 15,
            "valid_until": "2026-07-10",
            "min_purchase": 5000
        },
        {
            "id": "c007",
            "store": "Hamleys",
            "title": "Summer Fun Sale",
            "code": "PLAY20",
            "discount": 20,
            "valid_until": "2026-07-05",
            "min_purchase": 1500
        },
        {
            "id": "c008",
            "store": "Apple",
            "title": "Back to School",
            "code": "APPLELEARN",
            "discount": 10,
            "valid_until": "2026-08-31",
            "min_purchase": 20000
        }
    ]
    
    # Search analytics data
    search_queries = [
        {"query": "white shirt size M", "count": 284},
        {"query": "white sneakers under 5000", "count": 195},
        {"query": "ANC headphones noise cancel", "count": 123},
        {"query": "iphone 15 pro discount", "count": 98},
        {"query": "linen pants summer", "count": 62},
        {"query": "kids toys under 3000", "count": 58},
        {"query": "fossil watch leather", "count": 45},
        {"query": "nike air max black", "count": 42}
    ]
    
    return stores, products, coupons, search_queries


def init_session_state():
    """Initialize session state variables"""
    # Authentication states
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'profile_completed' not in st.session_state:
        st.session_state.profile_completed = False
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = None
    if 'user_otp_verified' not in st.session_state:
        st.session_state.user_otp_verified = False
    if 'generated_otp' not in st.session_state:
        st.session_state.generated_otp = None
    if 'login_stage' not in st.session_state:
        st.session_state.login_stage = 'phone'
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'gender': '',
            'age': None
        }
    
    # App states
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'shopper'
    if 'selected_store' not in st.session_state:
        st.session_state.selected_store = None
    if 'selected_store_key' not in st.session_state:
        st.session_state.selected_store_key = None
    if 'selected_store_label' not in st.session_state:
        st.session_state.selected_store_label = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'wishlist' not in st.session_state:
        st.session_state.wishlist = []
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []


# ============================================
# AUTHENTICATION & LOGIN FEATURES
# ============================================

def generate_otp():
    """Generate a random 6-digit OTP"""
    import random
    return str(random.randint(100000, 999999))

def render_login_page():
    """Render the login page with phone number and OTP verification"""
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #ffffff; margin-bottom: 0.5rem;">🛍️ MallQ</h1>
        <p style="color: #94a3b8; font-size: 1.2rem;">Your Perfect Shopping Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: #1a1a2e; padding: 2rem; border-radius: 16px; border: 1px solid #2d2d44;">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 1.5rem;">📱 Login</h2>
        """, unsafe_allow_html=True)
        
        if st.session_state.login_stage == 'phone':
            # Phone input stage
            st.markdown("**Enter Phone Number**")
            phone = st.text_input(
                "Phone Number",
                max_chars=10,
                placeholder="9876543210",
                label_visibility="collapsed",
                key="phone_input"
            )
            
            col_send, col_demo = st.columns(2)
            
            with col_send:
                if st.button("📨 Send OTP", width="stretch", key="send_otp_btn"):
                    if not phone:
                        st.error("❌ Please enter a phone number")
                    elif not phone.isdigit():
                        st.error("❌ Phone number must contain only digits")
                    elif len(phone) != 10:
                        st.error(f"❌ Phone number must be exactly 10 digits (you entered {len(phone)})")
                    else:
                        otp = generate_otp()
                        st.session_state.generated_otp = otp
                        st.session_state.phone_number = phone
                        st.session_state.login_stage = 'otp'
                        st.success(f"✅ OTP sent!")
                        st.info(f"**Demo OTP: {otp}** (for testing)")
                        st.rerun()
            
            with col_demo:
                st.info("💡 Demo mode enabled")
        
        elif st.session_state.login_stage == 'otp':
            # OTP verification stage
            st.markdown(f"**Verify OTP**")
            st.markdown(f"📱 Phone: +91-{st.session_state.phone_number}")
            st.markdown(f"*OTP sent to your phone*")
            
            st.divider()
            
            otp_input = st.text_input(
                "Enter 6-digit OTP",
                max_chars=6,
                placeholder="000000",
                label_visibility="collapsed",
                key="otp_input"
            )
            
            col_verify, col_resend = st.columns(2)
            
            with col_verify:
                if st.button("✅ Verify OTP", width="stretch", key="verify_otp_btn"):
                    if not otp_input:
                        st.error("❌ Please enter the OTP")
                    elif otp_input != st.session_state.generated_otp:
                        st.error("❌ Invalid OTP. Please try again.")
                    else:
                        st.session_state.user_otp_verified = True
                        st.session_state.login_stage = 'profile'
                        st.success("✅ OTP Verified!")
                        st.rerun()
            
            with col_resend:
                if st.button("🔄 Resend", width="stretch", key="resend_otp_btn"):
                    otp = generate_otp()
                    st.session_state.generated_otp = otp
                    st.info(f"New OTP: {otp}")
            
            if st.button("👈 Change Phone", width="stretch", key="change_phone_btn"):
                st.session_state.user_otp_verified = False
                st.session_state.phone_number = None
                st.session_state.generated_otp = None
                st.session_state.login_stage = 'phone'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)        
        st.markdown("</div>", unsafe_allow_html=True)


def render_profile_setup_page():
    """Render the user profile setup page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #ffffff; margin-bottom: 0.5rem;">👤 Complete Your Profile</h1>
        <p style="color: #94a3b8;">Help us personalize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: #1a1a2e; padding: 2rem; border-radius: 16px; border: 1px solid #2d2d44;">
            <h2 style="color: #ffffff; text-align: center; margin-bottom: 1.5rem;">📋 Profile Information</h2>
        """, unsafe_allow_html=True)
        
        # Full Name
        st.markdown("**Full Name** *")
        name = st.text_input(
            "Name",
            placeholder="Enter your full name",
            label_visibility="collapsed",
            max_chars=50,
            key="profile_name"
        )
        
        # Gender
        st.markdown("**Gender** *")
        gender = st.radio(
            "Gender",
            ["Male", "Female", "Other", "Prefer not to say"],
            horizontal=True,
            label_visibility="collapsed",
            key="profile_gender"
        )
        
        # Age
        st.markdown("**Age** *")
        age = st.slider(
            "Age",
            min_value=13,
            max_value=100,
            value=25,
            label_visibility="collapsed",
            key="profile_age"
        )
        
        # Phone display
        st.markdown(f"**📱 Phone:** +91-{st.session_state.phone_number}")
        
        st.divider()
        
        # Submit buttons
        col_submit, col_skip = st.columns(2)
        
        with col_submit:
            if st.button("✅ Complete Profile", width="stretch", key="complete_profile"):
                if not name or not name.strip():
                    st.error("❌ Name is required!")
                else:
                    st.session_state.user_profile = {
                        'name': name.strip(),
                        'gender': gender,
                        'age': age
                    }
                    st.session_state.profile_completed = True
                    st.session_state.is_logged_in = True
                    st.balloons()
                    st.success("✅ Welcome! Profile saved!")
                    st.rerun()
        
        with col_skip:
            if st.button("⏭️ Skip", width="stretch", key="skip_profile"):
                st.session_state.user_profile = {
                    'name': 'Guest User',
                    'gender': 'Not specified',
                    'age': None
                }
                st.session_state.profile_completed = True
                st.session_state.is_logged_in = True
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_user_menu():
    """Render user profile menu in the app"""
    with st.sidebar:
        st.markdown("""
        <div style="background: #1a1a2e; padding: 1rem; border-radius: 12px; border: 1px solid #2d2d44; margin-bottom: 1rem;">
        """, unsafe_allow_html=True)
        
        profile = st.session_state.user_profile
        st.markdown(f"👤 **{profile.get('name', 'User')}**")
        st.markdown(f"📱 +91-{st.session_state.phone_number}")
        st.markdown(f"👥 {profile.get('gender', 'N/A')} | 🎂 {profile.get('age', 'N/A')}")
        
        st.divider()
        
        if st.button("🚪 Logout", width="stretch"):
            st.session_state.is_logged_in = False
            st.session_state.profile_completed = False
            st.session_state.phone_number = None
            st.session_state.user_otp_verified = False
            st.session_state.generated_otp = None
            st.session_state.user_profile = {
                'name': '',
                'gender': '',
                'age': None
            }
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# HELPER FUNCTIONS
# ============================================

def format_price(price):
    """Format price in INR"""
    return f"₹{price:,}"

def calculate_savings(original, current):
    """Calculate savings amount"""
    return original - current

def get_category_color(category):
    """Return color for category"""
    colors = {
        "Fashion": "#f97316",
        "Footwear": "#22c55e",
        "Electronics": "#3b82f6",
        "Accessories": "#ec4899",
        "Toys": "#a855f7",
        "Dining": "#ef4444"
    }
    return colors.get(category, "#6b7280")

def filter_products(products, category=None, brand=None, price_range=None, color=None, search_query=None):
    """Filter products based on criteria"""
    filtered = products.copy()
    
    if category and category != "All":
        filtered = [p for p in filtered if p['category'] == category]
    
    if brand and brand != "All":
        filtered = [p for p in filtered if p['brand'] == brand]
    
    if price_range:
        min_price, max_price = price_range
        filtered = [p for p in filtered if min_price <= p['price'] <= max_price]
    
    if color and color != "All":
        filtered = [p for p in filtered if color.lower() in p['color'].lower()]
    
    if search_query:
        query = search_query.lower()
        filtered = [p for p in filtered if 
                   query in p['name'].lower() or 
                   query in p['brand'].lower() or
                   query in p['category'].lower() or
                   query in p['color'].lower()]
    
    return filtered


# ============================================
# UI COMPONENTS
# ============================================

def render_header():
    """Render the main header with navigation"""
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #7c3aed, #3b82f6); 
                        border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 20px;">🛍️</span>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.5rem; color: white;">MallQ!</h1>
                <p style="margin: 0; font-size: 0.8rem; color: #94a3b8;">Centralized Retail Directory & AI Planner</p>
            </div>
            <span style="background: #7c3aed; color: white; padding: 4px 12px; border-radius: 20px; 
                        font-size: 0.75rem; margin-left: 8px;">Mall Companion</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        nav_cols = st.columns(3)
        with nav_cols[0]:
            if st.button("🛒 Shopper Hub", width="stretch", 
                        type="primary" if st.session_state.current_view == 'shopper' else "secondary"):
                st.session_state.current_view = 'shopper'
                st.rerun()
        with nav_cols[1]:
            if st.button("🏪 Store Merchant", width="stretch",
                        type="primary" if st.session_state.current_view == 'merchant' else "secondary"):
                st.session_state.current_view = 'merchant'
                st.rerun()
        with nav_cols[2]:
            if st.button("⚙️ Mall Admin", width="stretch",
                        type="primary" if st.session_state.current_view == 'admin' else "secondary"):
                st.session_state.current_view = 'admin'
                st.rerun()
    
    st.markdown("<hr style='border-color: #2d2d44; margin: 1rem 0;'>", unsafe_allow_html=True)


def render_product_card(product, show_store=True):
    """Render a product card"""
    st.markdown(f"""
    <div class="product-card">
        <img src="{product['image']}" class="product-image" alt="{product['name']}" 
             onerror="this.src='[via.placeholder.com](https://via.placeholder.com/400x200?text=Product+Image)'">
        <div class="product-info">
            <p class="product-name">{product['name']}</p>
            <p class="product-brand">{product['brand']}{f" • {product['store']}" if show_store else ""}</p>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="product-price">{format_price(product['price'])}</span>
                <span class="product-original-price">{format_price(product['original_price'])}</span>
                <span style="background: #22c55e; color: white; padding: 2px 8px; border-radius: 4px; 
                            font-size: 0.75rem;">{product['discount']}% OFF</span>
            </div>
            <div style="margin-top: 8px; display: flex; align-items: center; gap: 8px;">
                <span style="color: #fbbf24;">★ {product['rating']}</span>
                <span style="color: #94a3b8; font-size: 0.85rem;">({product['reviews']} reviews)</span>
            </div>
            <div style="margin-top: 8px;">
                <span style="color: #94a3b8; font-size: 0.8rem;">Sizes: </span>
                {''.join([f'<span class="size-badge">{size}<span class="size-count">{qty}</span></span>' 
                         for size, qty in product['sizes'].items()])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_store_card(store):
    """Render a store card"""
    display_name = store.get('display_name', store['name'])
    st.markdown(f"""
    <div class="store-card" style="cursor: pointer;">
        <img src="{store['image']}" style="width: 100%; height: 150px; object-fit: cover;" 
             onerror="this.src='[via.placeholder.com](https://via.placeholder.com/400x150?text=Store+Image)'">
        <div class="store-badge">{store['level']}</div>
        <div style="padding: 1rem;">
            <h3 style="margin: 0; color: white; font-size: 1.1rem;">{display_name}</h3>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span style="background: {get_category_color(store['category'])}; color: white; 
                            padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">{store['category']}</span>
                <span class="store-rating">★ {store['rating']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# SHOPPER HUB VIEW
# ============================================

def render_shopper_view(stores, products, coupons):
    """Render the shopper hub interface"""
    
    # Hero Section
    alert_count = len([c for c in coupons if c['valid_until'] >= '2026-06-14'])
    st.markdown(f"""
    <div class="hero-section">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; 
                            font-size: 0.8rem;">COMPANION APP</span>
                <h1 class="hero-title" style="margin-top: 12px;">Centralized Mall Shopper Hub</h1>
                <p class="hero-subtitle">Compare prices, check real-time store size availability, 
                   run AI customized budget routing, and navigate with vectors.</p>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 12px 20px; border-radius: 12px; text-align: center;">
                <p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);">🔔 LIVE ALERTS DESK</p>
                <p style="margin: 4px 0 0 0; font-size: 1.2rem; font-weight: bold;">
                    {alert_count} New Alerts</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Directory & Inventory", 
        "🤖 AI Smart Planner & Budget Match", 
        "🏷️ Mall Offers & Promos",
        "🗺️ Visual Interactive Navigator Map"
    ])
    
    with tab1:
        render_directory_tab(stores, products)
    
    with tab2:
        render_ai_planner_tab(products, stores)
    
    with tab3:
        render_offers_tab(coupons, stores)
    
    with tab4:
        render_map_tab(stores)


def render_directory_tab(stores, products):
    """Render the directory and inventory tab"""
    
    col_filters, col_results = st.columns([1, 3])
    
    with col_filters:
        st.markdown("### 🔧 Refine Showcase")
        
        # Search
        search_query = st.text_input("🔍 Search store, shirts, sneaker...", key="dir_search")
        
        # Category filter
        st.markdown("**CATEGORY**")
        categories = ["All", "Fashion", "Footwear", "Electronics", "Toys", "Accessories"]
        selected_category = st.radio("Category", categories, horizontal=True, key="cat_filter", label_visibility="collapsed")
        
        # Level filter
        st.markdown("**LEVEL**")
        levels = ["All", "Ground", "First", "Second"]
        selected_level = st.radio("Level", levels, horizontal=True, key="level_filter", label_visibility="collapsed")
        
        st.markdown("---")
        
        # Live Price Compare Tool
        st.markdown("### 💰 LIVE PRICE COMPARE TOOL")
        st.markdown("Quick comparison of colors, cost and stores across the mall:")
        
        compare_item = st.selectbox("Select product type", 
                                    ["White Shirts", "Sneakers", "Jeans", "Watches", "T-Shirts"])
        
        if compare_item:
            if compare_item == "White Shirts":
                compare_products = [p for p in products if "shirt" in p['name'].lower() and "white" in p['color'].lower()]
            elif compare_item == "Sneakers":
                compare_products = [p for p in products if p['subcategory'] in ['Casual Sneakers', 'Running Shoes']]
            elif compare_item == "Jeans":
                compare_products = [p for p in products if p['category'] == 'Jeans']
            elif compare_item == "Watches":
                compare_products = [p for p in products if p['category'] == 'Watches']
            else:
                compare_products = [p for p in products if p['category'] == 'T-Shirts']
            
            if compare_products:
                compare_df = pd.DataFrame([
                    {"Store": p['store'], "Product": p['name'][:25]+"...", "Price": format_price(p['price'])}
                    for p in sorted(compare_products, key=lambda x: x['price'])[:5]
                ])
                st.dataframe(compare_df, hide_index=True, width="stretch")
    
    with col_results:
        # Filter stores
        filtered_stores = list(stores.values())
        if selected_category != "All":
            filtered_stores = [s for s in filtered_stores if s['category'] == selected_category]
        if selected_level != "All":
            filtered_stores = [s for s in filtered_stores if s['level'] == selected_level]
        
        st.markdown(f"### STORES MATCHING ({len(filtered_stores)})")
        
        # Display stores in grid
        store_cols = st.columns(2)
        for idx, store in enumerate(filtered_stores):
            with store_cols[idx % 2]:
                render_store_card(store)
                if st.button("View Products", key=f"view_{store['id']}"):
                    st.session_state.selected_store = store['id']
                    st.session_state.selected_store_key = store.get('store_key', store['name'])
                    st.session_state.selected_store_label = store.get('display_name', store['name'])
                    st.rerun()

                if st.session_state.selected_store == store['id']:
                    store_products_preview = [p for p in products if p['store'] == st.session_state.selected_store_key]
                    with st.expander(f"Products from {st.session_state.selected_store_label}", expanded=True):
                        if store_products_preview:
                            preview_cols = st.columns(2)
                            for prod_idx, product in enumerate(store_products_preview[:4]):
                                with preview_cols[prod_idx % 2]:
                                    render_product_card(product, show_store=False)
                        else:
                            st.info("No products available for this store.")
        
        st.markdown("---")
        
        # Product listing
        if st.session_state.selected_store:
            store_products = [p for p in products if p['store'] == st.session_state.selected_store_key]
            st.markdown(f"### Products from {st.session_state.selected_store_label} ({len(store_products)} items)")
        else:
            # Apply filters to products
            store_products = products.copy()
            if search_query:
                store_products = filter_products(store_products, search_query=search_query)
            if selected_category != "All":
                cat_map = {"Fashion": ["Shirts", "T-Shirts", "Pants", "Jeans"], 
                          "Footwear": ["Shoes"], "Electronics": ["Electronics"],
                          "Accessories": ["Watches"], "Toys": ["Toys"]}
                if selected_category in cat_map:
                    store_products = [p for p in store_products if p['category'] in cat_map[selected_category]]
            
            st.markdown(f"### All Products ({len(store_products)} items)")
        
        # Display products in grid
        prod_cols = st.columns(3)
        for idx, product in enumerate(store_products[:12]):  # Show first 12
            with prod_cols[idx % 3]:
                render_product_card(product, show_store=not st.session_state.selected_store)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🛒 Add", key=f"cart_{product['id']}", width="stretch"):
                        st.session_state.cart.append(product)
                        st.toast(f"Added {product['name']} to cart!")
                with col_b:
                    if st.button("❤️ Save", key=f"wish_{product['id']}", width="stretch"):
                        st.session_state.wishlist.append(product)
                        st.toast(f"Added to wishlist!")
        
        if st.session_state.selected_store:
            if st.button("← Back to All Stores"):
                st.session_state.selected_store = None
                st.session_state.selected_store_key = None
                st.session_state.selected_store_label = None
                st.rerun()


def render_ai_planner_tab(products, stores):
    """Render the AI Smart Planner tab"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 2rem; 
                border-radius: 16px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">🤖 AI Smart Shopping Planner</h2>
        <p style="color: #94a3b8; margin-top: 8px;">Tell us what you're looking for, 
           and we'll create a personalized shopping route within your budget.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### What are you looking for?")
        
        # Natural language input
        shopping_request = st.text_area(
            "Describe your shopping needs",
            placeholder="Example: I want to buy a white shirt and sneakers under ₹5000",
            height=100
        )
        
        st.markdown("### Or use quick filters:")
        
        filter_cols = st.columns(3)
        with filter_cols[0]:
            item_types = st.multiselect("Item Types", 
                                        ["Shirts", "T-Shirts", "Pants", "Jeans", "Shoes", "Watches", "Toys"])
        with filter_cols[1]:
            preferred_colors = st.multiselect("Preferred Colors",
                                             ["White", "Black", "Blue", "Grey", "Beige", "Multi"])
        with filter_cols[2]:
            budget = st.slider("Total Budget (₹)", 1000, 50000, 5000, step=500)
        
        if st.button("🚀 Generate Smart Shopping Plan", type="primary", width="stretch"):
            st.markdown("---")
            
            # Parse the request and filter products
            recommended = []
            
            if shopping_request:
                # Simple NLP parsing
                request_lower = shopping_request.lower()
                
                if "shirt" in request_lower:
                    shirts = [p for p in products if p['category'] == 'Shirts']
                    if "white" in request_lower:
                        shirts = [p for p in shirts if 'white' in p['color'].lower()]
                    recommended.extend(sorted(shirts, key=lambda x: x['price'])[:2])
                
                if "sneaker" in request_lower or "shoe" in request_lower:
                    shoes = [p for p in products if p['category'] == 'Shoes']
                    recommended.extend(sorted(shoes, key=lambda x: x['price'])[:2])
                
                if "jean" in request_lower:
                    jeans = [p for p in products if p['category'] == 'Jeans']
                    recommended.extend(sorted(jeans, key=lambda x: x['price'])[:2])
                
                if "watch" in request_lower:
                    watches = [p for p in products if p['category'] == 'Watches']
                    recommended.extend(sorted(watches, key=lambda x: x['price'])[:2])
                
                if "toy" in request_lower:
                    toys = [p for p in products if p['category'] == 'Toys']
                    recommended.extend(sorted(toys, key=lambda x: x['price'])[:2])
            
            elif item_types:
                for item_type in item_types:
                    items = [p for p in products if p['category'] == item_type or p['subcategory'] == item_type]
                    if preferred_colors:
                        items = [p for p in items if any(c.lower() in p['color'].lower() for c in preferred_colors)]
                    recommended.extend(sorted(items, key=lambda x: x['price'])[:2])
            
            if not recommended:
                # Default recommendations
                recommended = sorted(products, key=lambda x: x['rating'], reverse=True)[:6]
            
            # Filter by budget
            recommended = [p for p in recommended if p['price'] <= budget]
            
            # Calculate route
            total_cost = sum(p['price'] for p in recommended)
            total_savings = sum(p['original_price'] - p['price'] for p in recommended)
            unique_stores = list(set(p['store'] for p in recommended))
            
            st.markdown(f"""
            <div style="background: #22c55e; color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h3 style="margin: 0;">✨ Your Personalized Shopping Plan</h3>
                <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                    <div>
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Total Cost</p>
                        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{format_price(total_cost)}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">You Save</p>
                        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{format_price(total_savings)}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Stores to Visit</p>
                        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{len(unique_stores)}</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Budget Remaining</p>
                        <p style="margin: 0; font-size: 1.5rem; font-weight: bold;">{format_price(budget - total_cost)}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommended route
            st.markdown("### 📍 Recommended Route")
            
            for idx, store_name in enumerate(unique_stores):
                store = stores.get(store_name, {})
                store_items = [p for p in recommended if p['store'] == store_name]
                
                st.markdown(f"""
                <div style="background: #1a1a2e; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                            border-left: 4px solid #7c3aed;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="background: #7c3aed; color: white; padding: 4px 12px; 
                                        border-radius: 20px; font-size: 0.8rem;">Stop {idx + 1}</span>
                            <h4 style="margin: 8px 0 4px 0; color: white;">{store_name}</h4>
                            <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">
                                {store.get('level', 'Ground')} Floor • {len(store_items)} items
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; color: #22c55e; font-size: 1.2rem; font-weight: bold;">
                                {format_price(sum(p['price'] for p in store_items))}
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show items from this store
                item_cols = st.columns(len(store_items) if len(store_items) <= 3 else 3)
                for i, item in enumerate(store_items[:3]):
                    with item_cols[i]:
                        st.image(item['image'], width="stretch")
                        st.markdown(f"**{item['name'][:30]}...**")
                        st.markdown(f"{format_price(item['price'])}")
    
    with col2:
        st.markdown("### 🛒 Your Cart")
        if st.session_state.cart:
            cart_total = sum(p['price'] for p in st.session_state.cart)
            for item in st.session_state.cart:
                st.markdown(f"""
                <div style="background: #1a1a2e; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                    <p style="margin: 0; color: white; font-size: 0.9rem;">{item['name'][:25]}...</p>
                    <p style="margin: 4px 0 0 0; color: #22c55e;">{format_price(item['price'])}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #7c3aed; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="margin: 0; color: white;">Cart Total</p>
                <p style="margin: 4px 0 0 0; color: white; font-size: 1.5rem; font-weight: bold;">
                    {format_price(cart_total)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Clear Cart", width="stretch"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.info("Your cart is empty. Add items from the directory!")
        
        st.markdown("---")
        
        st.markdown("### ❤️ Wishlist")
        if st.session_state.wishlist:
            for item in st.session_state.wishlist[:5]:
                st.markdown(f"• {item['name'][:30]}... - {format_price(item['price'])}")
        else:
            st.info("Save items for later!")


def render_offers_tab(coupons, stores):
    """Render the offers and promos tab"""
    
    st.markdown("### 🏷️ Active Mall Offers & Promo Codes")
    
    # Filter coupons
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Filter by Store**")
        store_filter = st.selectbox("Store", ["All Stores"] + list(stores.keys()), key="promo_store_filter", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Sort by**")
        sort_option = st.radio("Sort", ["Highest Discount", "Expiring Soon", "Minimum Purchase"], 
                              horizontal=True, key="promo_sort", label_visibility="collapsed")
    
    # Filter and sort coupons
    filtered_coupons = coupons.copy()
    if store_filter != "All Stores":
        filtered_coupons = [c for c in filtered_coupons if c['store'] == store_filter]
    
    if sort_option == "Highest Discount":
        filtered_coupons = sorted(filtered_coupons, key=lambda x: x['discount'], reverse=True)
    elif sort_option == "Expiring Soon":
        filtered_coupons = sorted(filtered_coupons, key=lambda x: x['valid_until'])
    else:
        filtered_coupons = sorted(filtered_coupons, key=lambda x: x['min_purchase'])
    
    # Display coupons
    coupon_cols = st.columns(2)
    for idx, coupon in enumerate(filtered_coupons):
        with coupon_cols[idx % 2]:
            days_left = (datetime.strptime(coupon['valid_until'], '%Y-%m-%d') - datetime.now()).days
            
            st.markdown(f"""
            <div class="promo-card" style="background: linear-gradient(135deg, 
                {get_category_color(stores[coupon['store']]['category'])} 0%, 
                {get_category_color(stores[coupon['store']]['category'])}99 100%);">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0; font-size: 1rem;">{coupon['store']}</h4>
                        <p style="margin: 4px 0; font-size: 0.9rem; opacity: 0.9;">{coupon['title']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 2rem; font-weight: bold;">{coupon['discount']}%</span>
                        <p style="margin: 0; font-size: 0.8rem;">OFF</p>
                    </div>
                </div>
                <div style="margin-top: 1rem;">
                    <span class="promo-code">{coupon['code']}</span>
                </div>
                <div style="margin-top: 1rem; display: flex; justify-content: space-between; 
                            font-size: 0.85rem; opacity: 0.9;">
                    <span>Min. purchase: {format_price(coupon['min_purchase'])}</span>
                    <span>{'⚠️ ' if days_left <= 7 else ''}{days_left} days left</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📋 Copy Code", key=f"copy_{coupon['id']}", width="stretch"):
                st.toast(f"Code {coupon['code']} copied to clipboard!")


def render_map_tab(stores):
    """Render the visual navigator map tab"""
    
    st.markdown("### 🗺️ Interactive Mall Navigator")
    
    # Mall layout visualization
    st.markdown("""
    <div style="background: #1a1a2e; padding: 2rem; border-radius: 16px; text-align: center;">
        <h4 style="color: white; margin-bottom: 1rem;">Central Mall - Floor Layout</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a simple floor map using columns
    st.markdown("#### 🏢 Second Floor")
    second_floor = [s for s in stores.values() if s['level'] == 'Second']
    if second_floor:
        cols = st.columns(len(second_floor) if second_floor else 1)
        for idx, store in enumerate(second_floor):
            with cols[idx]:
                st.markdown(f"""
                <div style="background: {get_category_color(store['category'])}; padding: 1rem; 
                            border-radius: 8px; text-align: center; min-height: 80px;">
                    <p style="margin: 0; color: white; font-weight: bold;">{store['name']}</p>
                    <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.8rem;">
                        {store['category']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No stores on Second Floor")
    
    st.markdown("#### 🏢 First Floor")
    first_floor = [s for s in stores.values() if s['level'] == 'First']
    if first_floor:
        cols = st.columns(len(first_floor) if first_floor else 1)
        for idx, store in enumerate(first_floor):
            with cols[idx]:
                st.markdown(f"""
                <div style="background: {get_category_color(store['category'])}; padding: 1rem; 
                            border-radius: 8px; text-align: center; min-height: 80px;">
                    <p style="margin: 0; color: white; font-weight: bold;">{store['name']}</p>
                    <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.8rem;">
                        {store['category']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("#### 🏢 Ground Floor")
    ground_floor = [s for s in stores.values() if s['level'] == 'Ground']
    if ground_floor:
        cols = st.columns(len(ground_floor) if ground_floor else 1)
        for idx, store in enumerate(ground_floor):
            with cols[idx]:
                st.markdown(f"""
                <div style="background: {get_category_color(store['category'])}; padding: 1rem; 
                            border-radius: 8px; text-align: center; min-height: 80px;">
                    <p style="margin: 0; color: white; font-weight: bold;">{store['name']}</p>
                    <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.8rem;">
                        {store['category']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Legend
    st.markdown("---")
    st.markdown("#### 🎨 Category Legend")
    legend_cols = st.columns(6)
    categories = [("Fashion", "#f97316"), ("Footwear", "#22c55e"), ("Electronics", "#3b82f6"),
                 ("Accessories", "#ec4899"), ("Toys", "#a855f7"), ("Dining", "#ef4444")]
    for idx, (cat, color) in enumerate(categories):
        with legend_cols[idx]:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 16px; height: 16px; background: {color}; border-radius: 4px;"></div>
                <span style="color: #94a3b8; font-size: 0.85rem;">{cat}</span>
            </div>
            """, unsafe_allow_html=True)


# ============================================
# MERCHANT CONSOLE VIEW
# ============================================

def render_merchant_view(stores, products, coupons):
    """Render the store merchant console"""
    
    st.markdown("""
    <div class="hero-section" style="background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);">
        <span style="background: #22c55e; color: white; padding: 4px 12px; border-radius: 20px; 
                    font-size: 0.8rem;">MERCHANT CONSOLE</span>
        <h1 class="hero-title" style="margin-top: 12px;">Store & Inventory Central</h1>
        <p class="hero-subtitle">Manage your store details, alter prices instantly, and add deals to attract physical shoppers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Store selector
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("**ACTIVE WORKSPACE**")
        selected_merchant = st.selectbox("Select Your Store", list(stores.keys()), key="merchant_store")
    
    store = stores[selected_merchant]
    store_products = [p for p in products if p['store'] == selected_merchant]
    store_coupons = [c for c in coupons if c['store'] == selected_merchant]
    
    # Analytics section
    st.markdown(f"### 📊 {selected_merchant} Footfall Analytics")
    
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Catalog Views", f"{random.randint(800, 1500):,}", f"+{random.randint(5, 15)}%")
    with metric_cols[1]:
        st.metric("Size Checks", f"{random.randint(300, 700)}", f"+{random.randint(3, 12)}%")
    with metric_cols[2]:
        st.metric("Wishlist Adds", f"{random.randint(50, 150)}", f"+{random.randint(2, 8)}%")
    with metric_cols[3]:
        st.metric("Store Visits", f"{random.randint(200, 500)}", f"+{random.randint(5, 20)}%")
    
    # Recent queries
    st.markdown("**RECENT QUERIES MATCH**")
    queries = [
        (f"{store.get('category', 'product').lower()} {selected_merchant.lower()}", random.randint(50, 150)),
        (f"oversized {store.get('category', 'item').lower()}", random.randint(30, 100))
    ]
    for query, hits in queries:
        st.markdown(f"""
        <div class="query-bar">
            <span class="query-text">"{query}"</span>
            <span class="query-count">{hits} hits</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two column layout
    col_inventory, col_promo = st.columns([2, 1])
    
    with col_inventory:
        st.markdown(f"### 📦 Catalog Management ({len(store_products)} items listed)")
        
        for product in store_products[:5]:
            with st.expander(f"{product['name']} - {format_price(product['price'])}", expanded=False):
                inv_cols = st.columns([1, 3])
                with inv_cols[0]:
                    st.image(product['image'], width="stretch")
                with inv_cols[1]:
                    new_price = st.number_input(
                        "Listing Price (₹)", 
                        value=product['price'], 
                        key=f"price_{product['id']}",
                        step=100
                    )
                    
                    st.markdown("**SIZE STOCK COUNTS**")
                    size_cols = st.columns(len(product['sizes']))
                    for idx, (size, qty) in enumerate(product['sizes'].items()):
                        with size_cols[idx]:
                            new_qty = st.number_input(size, value=qty, key=f"size_{product['id']}_{size}", 
                                                     min_value=0, max_value=100)
                    
                    if st.button("Update Product", key=f"update_{product['id']}"):
                        st.success("Product updated successfully!")
        
        # Add new product form
        st.markdown("---")
        st.markdown("### ➕ Spawn New Catalog Item")
        
        with st.form("new_product_form"):
            np_cols = st.columns(2)
            with np_cols[0]:
                new_title = st.text_input("Product Title", placeholder="e.g., Vintage Denim Overcoat")
                new_price_input = st.number_input("Price (₹)", value=2499, step=100)
                new_category = st.selectbox("Category Section", 
                                           ["Fashion / Clothing", "Footwear", "Accessories", "Electronics", "Toys"])
            with np_cols[1]:
                new_color = st.text_input("Color", value="Beige")
                new_sizes = st.text_input("Sizes (comma-separated)", value="S, M, L, XL")
            
            submitted = st.form_submit_button("📤 Publish to Mall Catalog", width="stretch")
            if submitted:
                st.success(f"'{new_title}' has been added to the catalog!")
    
    with col_promo:
        st.markdown("### 🎫 Targeted Promotional Coupons")
        
        # Existing coupons
        st.markdown("**ACTIVE STORE COUPONS**")
        for coupon in store_coupons:
            st.markdown(f"""
            <div class="coupon-active">
                <p style="margin: 0; font-weight: bold;">{coupon['title']}</p>
                <p style="margin: 4px 0 0 0; font-family: monospace;">Code: {coupon['code']}</p>
                <p style="margin: 4px 0 0 0; font-size: 0.85rem; opacity: 0.9;">
                    {coupon['discount']}% off • Min {format_price(coupon['min_purchase'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add new coupon
        st.markdown("**ADD LIVE COUPON**")
        with st.form("new_coupon_form"):
            promo_title = st.text_input("Promo Heading Title", placeholder="Summer Special Discount")
            promo_cols = st.columns(2)
            with promo_cols[0]:
                promo_discount = st.number_input("Discount %", value=20, min_value=5, max_value=70)
            with promo_cols[1]:
                promo_code = st.text_input("Voucher Code", placeholder="SUMMER20")
            
            if st.form_submit_button("💳 Deploy Coupon Code", width="stretch"):
                st.success(f"Coupon '{promo_code}' is now live!")


# ============================================
# ADMIN CONSOLE VIEW
# ============================================

def render_admin_view(stores, products, coupons, search_queries):
    """Render the mall administration console"""
    
    st.markdown("""
    <div class="hero-section" style="background: linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%);">
        <span style="background: #f97316; color: white; padding: 4px 12px; border-radius: 20px; 
                    font-size: 0.8rem;">MALL ADMINISTRATION LOGINS</span>
        <h1 class="hero-title" style="margin-top: 12px;">MallQ! Management Console</h1>
        <p class="hero-subtitle">Review live footfall, adjust central directories, and analyze shopper feedbacks to advise store owners.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    admin_tab = st.radio("Admin", ["📊 Dashboard", "⚙️ Configure", "👥 Shopper"], 
                        horizontal=True, key="admin_tab", label_visibility="collapsed")
    
    if admin_tab == "📊 Dashboard":
        # Key metrics
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.markdown("""
            <div class="stat-card">
                <p class="stat-label">TOTAL MAPPED STORES</p>
                <p class="stat-value">8 Active</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">Central mall contains 42 registers.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
            <div class="stat-card">
                <p class="stat-label">ESTIMATED MALL FOOTFALL</p>
                <p class="stat-value">14,500</p>
                <p class="stat-subtext">📈 +12% increase from last Sunday</p>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(f"""
            <div class="stat-card">
                <p class="stat-label">ACTIVE PROMO COUPONS</p>
                <p class="stat-value">{len(coupons)} Code sets</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">Coupons deployed across catalog shops.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            st.markdown("""
            <div class="stat-card">
                <p class="stat-label">FEEDBACK REVIEWS</p>
                <p class="stat-value">2 filings</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">100% checked by center reception.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Analytics section
        col_queries, col_segments = st.columns(2)
        
        with col_queries:
            st.markdown("""
            <div class="dashboard-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <p class="dashboard-title">Consumer Intended Queries Analysis</p>
                    <span style="background: #7c3aed; color: white; padding: 4px 10px; 
                                border-radius: 20px; font-size: 0.7rem;">TOP TRAFFIC HITS</span>
                </div>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;">
                    Analyzing search trends allows administrators to coordinate mall layout planning and inventory allocations.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            max_count = max(q['count'] for q in search_queries)
            for query in search_queries:
                progress = (query['count'] / max_count) * 100
                st.markdown(f"""
                <div class="query-bar">
                    <span class="query-text">"{query['query']}"</span>
                    <span class="query-count">{query['count']} searches</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%;"></div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_segments:
            st.markdown("""
            <div class="dashboard-card">
                <p class="dashboard-title">Central Store Segment Distributions</p>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1rem;">
                    Based on current on-board catalog listings:
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            segments = [
                ("Fashion", "#f97316", "45%"),
                ("Footwear", "#22c55e", "20%"),
                ("Electronics", "#3b82f6", "15%"),
                ("Dining", "#ef4444", "12%"),
                ("Accessories", "#ec4899", "8%")
            ]
            
            for name, color, percentage in segments:
                st.markdown(f"""
                <div class="segment-row">
                    <div style="display: flex; align-items: center;">
                        <span class="segment-dot" style="background: {color};"></span>
                        <span style="color: white;">{name}</span>
                    </div>
                    <span style="color: #94a3b8;">{percentage} of shops</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Footfall trend chart
            st.markdown("---")
            st.markdown("**Weekly Footfall Trend**")
            
            # Simple bar chart data
            footfall_data = {
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'Visitors': [8500, 9200, 8800, 9500, 11200, 14500, 13800]
            }
            st.bar_chart(pd.DataFrame(footfall_data).set_index('Day'))
    
    elif admin_tab == "⚙️ Configure":
        st.markdown("### ⚙️ Mall Configuration")
        
        config_cols = st.columns(2)
        
        with config_cols[0]:
            st.markdown("#### Store Directory Management")
            
            for store_name, store in stores.items():
                with st.expander(f"{store_name} ({store['level']} Floor)"):
                    st.text_input("Store Name", value=store['name'], key=f"cfg_name_{store['id']}")
                    st.selectbox("Floor Level", ["Ground", "First", "Second"], 
                                index=["Ground", "First", "Second"].index(store['level']),
                                key=f"cfg_level_{store['id']}")
                    st.selectbox("Category", ["Fashion", "Footwear", "Electronics", "Accessories", "Toys", "Dining"],
                                key=f"cfg_cat_{store['id']}")
                    if st.button("Update Store", key=f"cfg_update_{store['id']}"):
                        st.success(f"{store_name} configuration updated!")
        
        with config_cols[1]:
            st.markdown("#### Add New Store")
            
            with st.form("add_store_form"):
                new_store_name = st.text_input("Store Name")
                new_store_level = st.selectbox("Floor Level", ["Ground", "First", "Second"])
                new_store_cat = st.selectbox("Category", 
                                            ["Fashion", "Footwear", "Electronics", "Accessories", "Toys", "Dining"])
                
                if st.form_submit_button("➕ Add Store to Directory"):
                    st.success(f"'{new_store_name}' has been added to the mall directory!")
            
            st.markdown("---")
            st.markdown("#### Mall Operating Hours")
            
            op_cols = st.columns(2)
            with op_cols[0]:
                st.time_input("Opening Time", value=datetime.strptime("10:00", "%H:%M").time())
            with op_cols[1]:
                st.time_input("Closing Time", value=datetime.strptime("22:00", "%H:%M").time())
    
    else:  # Shopper tab
        st.markdown("### 👥 Shopper Analytics & Feedback")
        
        # Recent feedbacks
        st.markdown("#### Recent Feedback Submissions")
        
        feedbacks = [
            {"user": "Anonymous", "store": "Nike", "rating": 5, "comment": "Great collection and helpful staff!", 
             "date": "2026-06-13"},
            {"user": "Anonymous", "store": "ZARA", "rating": 4, "comment": "Good variety but crowded on weekends.", 
             "date": "2026-06-12"}
        ]
        
        for feedback in feedbacks:
            st.markdown(f"""
            <div style="background: #1a1a2e; padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                        border-left: 4px solid #22c55e;">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <span style="color: white; font-weight: bold;">{feedback['store']}</span>
                        <span style="color: #fbbf24; margin-left: 8px;">{'★' * feedback['rating']}</span>
                    </div>
                    <span style="color: #94a3b8; font-size: 0.85rem;">{feedback['date']}</span>
                </div>
                <p style="color: #94a3b8; margin: 8px 0 0 0;">"{feedback['comment']}"</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Shopper demographics (simulated)
        st.markdown("#### Shopper Demographics (This Week)")
        
        demo_cols = st.columns(3)
        with demo_cols[0]:
            st.markdown("**Age Distribution**")
            age_data = {'Age': ['18-24', '25-34', '35-44', '45+'], 'Percentage': [25, 35, 25, 15]}
            st.bar_chart(pd.DataFrame(age_data).set_index('Age'))
        
        with demo_cols[1]:
            st.markdown("**Peak Hours**")
            hours_data = {'Hour': ['10-12', '12-14', '14-16', '16-18', '18-20', '20-22'],
                         'Visitors': [800, 1200, 1500, 1800, 2200, 1600]}
            st.bar_chart(pd.DataFrame(hours_data).set_index('Hour'))
        
        with demo_cols[2]:
            st.markdown("**Visit Purpose**")
            purpose_data = [
                ("Shopping", 55),
                ("Dining", 25),
                ("Entertainment", 15),
                ("Services", 5)
            ]
            for purpose, pct in purpose_data:
                st.markdown(f"{purpose}: **{pct}%**")
                st.progress(pct / 100)


# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application entry point"""
    
    # Initialize session state
    init_session_state()
    
    # Show login flow if not authenticated
    if not st.session_state.is_logged_in:
        if st.session_state.login_stage == 'phone' or st.session_state.login_stage == 'otp':
            render_login_page()
        elif st.session_state.login_stage == 'profile':
            render_profile_setup_page()
        else:
            render_login_page()
        return
    
    # User is logged in - show main app
    # Load data
    stores, products, coupons, search_queries = load_mall_data()
    
    # Show user menu in sidebar
    render_user_menu()
    
    # Render header
    render_header()
    
    # Render appropriate view based on navigation
    if st.session_state.current_view == 'shopper':
        render_shopper_view(stores, products, coupons)
    elif st.session_state.current_view == 'merchant':
        render_merchant_view(stores, products, coupons)
    else:  # admin
        render_admin_view(stores, products, coupons, search_queries)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #94a3b8; padding: 1rem;">
        <p>MallQ! Mall Companion App © 2026 | Centralized Retail Directory & AI Planner</p>
        <p style="font-size: 0.85rem;">Built for enhancing physical retail shopping experiences</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
