from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/remote_interview_db"
mongo = PyMongo(app)

# Folder to save profile pictures
UPLOAD_FOLDER = 'static/profile_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # Hash the password
        bio = request.form['bio']
        skills = request.form['skills'].split(',')  # Convert to list
        employment = request.form['employment']

        # Handle profile picture upload
        profile_picture = request.files['profile_picture']
        profile_picture_filename = secure_filename(profile_picture.filename)
        profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
        
        try:
            profile_picture.save(profile_picture_path)
        except Exception as e:
            # Handle file upload error (log it, notify user, etc.)
            return "Error saving the profile picture."

        # Store user data in MongoDB
        user_data = {
            'name': name,
            'email': email,
            'password': password,  # Already hashed
            'bio': bio,
            'skills': skills,
            'employment': employment,
            'profile_picture': profile_picture_path,
        }

        # Insert user data into the MongoDB collection
        mongo.db.users.insert_one(user_data)

        # Redirect to the dashboard
        user = mongo.db.users.find_one({"email": email})
        if user:
            return redirect(url_for('dashboard', user_id=user['_id']))
        else:
            # Handle user not found error
            return "User not found."

    return render_template('createAccount.html')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    # Retrieve user data from MongoDB
    user_data = mongo.db.users.find_one({"_id": user_id})

    # Sample data for demonstration
    data = {
        'User ID': [1, 2, 3, 1, 2, 3],
        'Interview Date': pd.to_datetime(['2024-10-01', '2024-10-01', '2024-10-02', '2024-10-15', '2024-10-15', '2024-10-16']),
        'Score': [85, 90, 75, 95, 88, 80],
        'Feedback': [
            'Great job on technical skills!',
            'Good communication skills!',
            'Needs improvement in problem-solving.',
            'Excellent presentation and clarity.',
            'Strong answers, keep practicing!',
            'Focus on time management.'
        ],
        'Areas of Improvement': [
            'None',
            'None',
            'Problem-solving',
            'None',
            'None',
            'Time management'
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Create visualizations
    plt.figure(figsize=(10, 5))

    # Pie chart for average scores
    avg_scores = df.groupby('User ID')['Score'].mean()
    labels = avg_scores.index
    sizes = avg_scores.values

    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Average Scores by User')

    # Bar chart for scores over time
    plt.subplot(1, 2, 2)
    df.groupby('Interview Date')['Score'].mean().plot(kind='bar', color='skyblue')
    plt.title('Average Scores Over Time')
    plt.xlabel('Interview Date')
    plt.ylabel('Average Score')

    plt.tight_layout()
    
    # Save the figure
    plt.savefig('static/dashboard.png')  # Save the figure in the static folder
    plt.close()  # Close the plot to avoid displaying it

    return render_template('dashboard.html', user_data=user_data, image_path='static/dashboard.png')

if __name__ == "__main__":
    app.run(debug=True)
