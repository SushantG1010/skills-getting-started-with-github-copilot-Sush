"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
        "Soccer Team": {
        "description": "Practice skills, build teamwork, and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Swimming Club": {
        "description": "Improve endurance and technique through team practices",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Drama Club": {
        "description": "Explore acting, stagecraft, and performance techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "School Band": {
        "description": "Play instruments and prepare for school performances",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 24,
        "participants": []
    },
    "Science Olympiad": {
        "description": "Solve challenges in biology, chemistry, and physics",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
