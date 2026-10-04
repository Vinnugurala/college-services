# College Services

A Django web app that helps hostel students skip queues. Students pre-order food from hostel canteens and food stalls, and send print jobs to campus xerox shops.

## The problem
Students waste time standing in line at canteens and xerox shops. This app lets them order first and collect later.

## Features
- Students: register, log in, browse canteens, add items to a cart, place orders, track orders
- Canteen/stall owners: register their canteen, add and manage menu items
- Xerox shop owners: register their shop and manage print orders
- Students upload files and send them to a registered xerox shop
- Admin dashboard for managing the site
- Payment page (VERIFY: say what it really does, or delete this line)

## Tech stack
Python, Django, MySQL, HTML, CSS, JavaScript

## How to run it locally
1. Clone the repo:
   git clone https://github.com/Vinnugurala/college-services.git
   cd college-services
2. Create a virtual environment and install packages:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
3. Create a MySQL database (for example `college_services`).
4. Copy `.env.example` to `.env` and fill in your values:
   copy .env.example .env
5. Create the tables:
   python manage.py migrate
6. Start the server:
   python manage.py runserver
7. Open http://127.0.0.1:8000

## Project status
Local development only. Not deployed.

## Author
Gurala Durga Vara Prasad
