# NLP Resume Classifier
Welcome to My Project! This repository contains NLP based resume classifier in a plug and play manner. The code just need a resume pdf directory, then it automatically categorize each resume and save in a appropriate created folder. This project will help a lot in employee recruitment system.

## Setup Instructions

Follow these steps to set up your development environment and run the project:

### Prerequisites

- Python 3.8.17 or later
- Git (for cloning the repository)

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/ahsanimran-academic/NLP_resume_classifier.git
```
### Step 2: Create and Activate a Virtual Environment
Navigate to the project directory and create a virtual environment:

```bash
cd NLP_resume_classifier
```
For Windows:
```bash
python -m venv myenv
myenv\Scripts\activate
```
For Linux and macOS:
```bash
python3 -m venv myenv
source myenv/bin/activate
```
### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```
### Step 4: Run the Project
Now you need to have a directory. The directory should contain some PDF resumes. The code will automatically create folders according to their category and place them there. This code will also create a 'categorized_resumes.csv' file in the same directory.

```bash
python script.py path/to/dir
```
For example, as the terminal is opened in the same cloned repo directory and the resumes are in the folder named 'test_resume', I executed the command:
```bash
python script.py test_resume
```
