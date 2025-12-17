# Shopy-Shop 

**Shopy-Shop** is a simple e-commerce website built with Django. The site lets users browse products, view details, add to cart, and complete checkout. 

##  Features 

- Product listing (catalogue)  
- Product detail pages (with name, description, price, image)  
- Shopping cart functionality (add/remove products, quantity)  
- Basic order/checkout flow  
- Admin dashboard (via Django admin) to manage products and orders  


## Prerequisites

- Python 3.x  
- pip  
- virtualenv (recommended)  

## Installation & Running Locally

1. Clone the repo  
   ```bash
   git clone https://github.com/Memory-Wabwile/Shopy-Shop.git
   cd Shopy-Shop

2. (Optional but recommended) Create a virtual environment and activate it
   ```bash
    python -m venv venv         # or `python3 -m venv venv`  
    source venv/bin/activate    # On Windows: `venv\Scripts\activate`  


4. Install dependencies
   ```bash
    pip install -r requirements.txt


6. Apply migrations and start the server
   ```bash
    python manage.py migrate  
    python manage.py runserver

8. In your browser, go to http://127.0.0.1:8000/ to see the site

