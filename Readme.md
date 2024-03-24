# Period Tracking Application:
This is a web application for tracking menstrual periods. Users can register, log in, record their period details, view their period history, predict future periods, and analyze symptoms.

## Features:
- User Authentication: Users can register with their email and password, and then log in securely using JWT authentication.
- Period Tracking: Users can record the start and end dates of their menstrual periods, as well as any associated symptoms.
- Period History: Users can view their past periods and associated details.
- Period Prediction: The application can predict the start date of the next period based on past data.
- Symptom Analysis: Users can analyze the frequency of symptoms experienced during their periods using visualizations. A pdf will be downloaded showing frequency of different symptoms, and also a heatmap showing correlation between different symptoms.
  
## Technologies Used:
- Backend: Django REST Framework, Python
- Frontend: React (or Django templates if frontend is developed using Django)
- Database: PostgreSQL (or other supported by Django ORM)
- Authentication: JWT (JSON Web Tokens)
- Data Visualization: Matplotlib, Seaborn (for backend), React components (for frontend)
- Other Libraries: Pandas, ReportLab
