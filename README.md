# Chatbot and Calendar Project

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

3. **Slot Constraints**

## DB Migration
To create db tables 
- python3 manage.py makemigrations
- python3 manage.py migrate