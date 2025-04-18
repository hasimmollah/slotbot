# Slotbot: Chatbot-Powered Calendar Scheduling App

This project is built using **Django** for the backend, **React** for the frontend, and **Python** to handle business logic and data management. The main purpose of this project is to create a **chatbot** that allows users to query available **interview slots** for a company and display those slots both in the chat window and on an integrated calendar.

## Project Overview

The application allows users to:

- **Query available slots** for a specific company.
- **Specify parameters** such as the number of days and duration of the slots.
- **View the available slots** in both the chat window and on a calendar interface.
- The system ensures that **overlapping slots** are not scheduled, with each company limited to a maximum of **3 slots per day**.
- Slots are scheduled only between **8 AM and 5 PM**, with no slots allowed during **12 PM - 1 PM** (lunch break), and weekends are excluded.

## Key Features

1. **Chatbot Integration**:
   - Users can type specific prompts like **"Show slots for ABC Company"**, and the chatbot will fetch available slots and display them.
   - Users can specify additional parameters like **duration** and **number of days** when querying the available slots.

2. **Calendar Integration**:
   - Available slots for each company are shown on an interactive calendar, making it easy for users to view the scheduled times.
   - The calendar shows the slots in **hourly** increments, ensuring the schedule is easy to manage and understand.
3. **Slot Constraints**:
   - Maximum of 3 slots per day per company
   - No overlapping slots: Each slot must be scheduled without conflicts with other slots.
   - Slot duration: Slots are created with a duration specified by the user (e.g., 1 hour, 2 hours).
   - Allowed hours: Slots can only be scheduled between 8 AM - 5 PM on weekdays. The 12 PM - 1 PM time block is unavailable due to the lunch break.
4. **Flexible Slot Scheduling**:
   - The system allows users to specify custom slot durations and can schedule them consecutively if possible. If no slots are available at the requested time, the system will try to fit the requested duration in the next available time slot.

## Technologies Used
- **Backend**:
  - **Django**: A high-level Python web framework to handle the backend API and data storage (PostgreSQL or SQLite as the database).
- **Frontend**:
  - **React**: JavaScript library for building the user interface (UI), including the chatbot interface and calendar view.
  - **React-Big-Calendar**: A library to render the calendar with available slots.
- **Python**:
  - Used to handle the slot generation logic, including duration handling, checking for overlapping slots, and formatting the data to be displayed on the frontend.

## Installation

### Prerequisites

1. **Python 3.x** - For the Django backend.
2. **Node.js** - For the React frontend.
3. **Git** - For version control.

### Steps to Set Up

1. **Clone the repository**:
   ```bash
   git clone git@github.com:hasimmollah/slotbot.git
   cd slotbot
2. **Set up the Django backend**:
   - Create a virtual environment for Python:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`

3. **DB Migration**:
   - Need to run below command to prepare tables
   ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
   
4. **Set up the React frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   
5. **Run the Django backend**:
    ```bash
   copy `dist` folder from frontend to backend directory
   cd ..
   python3 manage.py runserver

## Usage
1. **Viewing Slots via Chatbot**:
   - Type commands such as "Show slots for [Company Name]" in the chatbot interface.
   - You can specify the number of days and duration using prompts like:
     - "Show slots for ABC Company for 4 days"
     - "Show slots for XYZ Company for 7 days for duration 2:00 hours"
2. **Viewing Slots on the Calendar**:
   - Available slots will also be shown in the calendar view on the frontend.
   - The calendar will display the slots scheduled for each company in the specified date range.

## Slot Scheduling Rules 
- Company Slots: Each company can have a maximum of 3 slots per day.
- No Overlapping: Slots cannot overlap with each other. If a slot overlaps, the system will try to find the next available time.
- No Weekend Slots: Slots can only be scheduled on weekdays (Monday to Friday).
- Lunch Break Exclusion: No slots can be scheduled from 12 PM - 1 PM (lunch break).
- Working Hours: Available slots can only be between 8 AM - 5 PM.

## API Endpoints
1. GET /api/slots:
   - Fetch all available slots from the backend.
   - Returns a list of slots with company, date, start_time, and end_time.
2. POST /api/slots:
   - Endpoint to create a new interview slot for a company.

## Future Improvements
- Authentication: Implement user authentication so that only authorized users can schedule slots.
- Admin Panel: Create an admin interface to manage slots for different companies.
- Mobile Support: Improve the responsiveness of the frontend to support mobile devices.
- Slot Conflict Resolution: Enhance the slot conflict resolution logic with more granular control over scheduling.
- Deleting slot from calendar
