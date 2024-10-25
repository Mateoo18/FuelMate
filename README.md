# FuelMate

FuelMate is a web application designed to help users locate nearby fuel stations with the best prices based on their location or a manually entered address. The app allows registered users to save their favorite stations for quick access, providing up-to-date fuel prices sourced from a managed database.

## Features

### User Features
- **Locate Nearby Stations**: Detects user's location and displays nearby fuel stations with current fuel prices.
- **Search by Address**: Allows users to manually enter an address if location sharing is disabled.
- **Favorite Stations**: Registered users can mark stations as "favorite" for easy access.
- **User Authentication**: Users can create an account, log in, and view their saved stations.
- **Update Gas Prices**: Users can update gas prices on diffrent gas stations.

### Admin Features
- **Manage Stations**: Admins can add, edit, or delete stations in the database.
- **Update Fuel Prices**: Admins can update fuel prices to ensure accuracy.
- **User Management**: Manage user accounts and monitor app activity logs.

## Architecture Overview

The application is built with a **Django backend** and a **HTML/CSS/JavaScript frontend** integrated with Google Maps API for geolocation services.

### Stack
- **Backend**: Django (Python) for handling requests, data processing, and database interactions.
- **Frontend**: HTML, CSS, JavaScript for the user interface and dynamic updates.
- **Database**: PostgreSQL or MySQL for secure data storage.
- **External APIs**: Google Maps API for geolocation services and directions.

