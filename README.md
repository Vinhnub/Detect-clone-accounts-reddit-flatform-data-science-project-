🧠 Introduction:

    + This project builds an AI system to detect spam accounts on Reddit based on user and post data.
    The goal is to classify Reddit accounts as "normal" or "spam" using statistical features (karma, account age, posting frequency, etc.) and machine learning models.


🚀 Features:

    + 🧩 Collect user and post data from the Reddit API (Automaticly).

    + 🧮 Data preprocessing and cleaning (remove duplicates, normalize values).

    + 🤖 Train Machine Learning models to detect spam accounts.

    + 📊 Visualize data and classification results.

    + ☁️ Automatic periodic updates and data storage using GitHub Actions.


🗂️ Project Structure:

    ```
    
    ├── 📁 .git/ 🚫 (auto-hidden)

    ├── 📁 .github/

    │   └── 📁 workflows/

    │       ├── ⚙️ auto.yml

    │       └── ⚙️ settings.yaml

    ├── 📁 crawReditRender/

    │   ├── 🐍 crawRedit.py

    │   └── 📄 requirements.txt

    ├── 📁 database/

    │   ├── 📁 image/

    │   │   ├── 🖼️ ERD.png

    │   │   └── 🖼️ diagram.png

    │   ├── 🐍 __init__.py

    │   ├── 🐍 database_access.py

    │   └── 🗄️ query.sql

    ├── 📁 get_data/

    │   ├── 🐍 __init__.py

    │   ├── 🐍 auth.py

    │   ├── 🐍 constants.py

    │   ├── 🐍 database_fetcher.p
    y
    │   ├── 🐍 get_data_user_by_requests.py

    │   ├── 🐍 reddit_crawler.py

    │   └── 🐍 reddit_crawler_to_sqlite.py

    ├── 📁 utils/

    │   ├── 🐍 __init__.py

    │   ├── 📄 ggdrive-api-key.json 🚫 (auto-hidden)

    │   ├── 📄 ggdrive_access_token.json 🚫 (auto-hidden)

    │   ├── 📄 ggdrive_token.json 🚫 (auto-hidden)

    │   └── 🐍 secrets.py 🚫 (auto-hidden)

    ├── 🚫 .gitignore

    ├── 📖 README.md

    └── 📄 requirements.txt

    ```

    ---


⚙️ Installation:

    1️⃣ Clone repository: 

                        - git clone https://github.com/yourusername/reddit-spam-detector.git

                        - cd reddit-spam-detector

    2️⃣ Create virtual environment (optional):

                        - python -m venv venv

                        - source venv/bin/activate      # Windows: venv\Scripts\activate

    3️⃣ Install dependencies:

                        - pip install -r requirements.txt

    4️⃣ Configure Reddit API:
    
                        - Create config.json:
                        {
                        "client_id": "YOUR_CLIENT_ID",
                        "client_secret": "YOUR_CLIENT_SECRET",
                        "user_agent": "RedditSpamDetector/1.0"
                        }
    
    5️⃣ Set up and connect to database (SQL-Server), run file reddit_crawler.py 

⚙️ Installation Automatic:
    1️⃣ Set up file .yml for github action. 

    2️⃣ Get and set up Google API to access Google Drive

    3️⃣ Use github action to run file reddit_crawler_to_sqlite.py

🤝 Contributing:

    1. Fork the repository

    2. Create a new branch (git checkout -b feature/new-feature)

    3. Commit your changes (git commit -m "Add new feature")

    4. Push and create a Pull Request


📜 License:

    + None


📧 Contact:

    + 👤 Nguyen Van Vinh

    + 📩 Email: vinhvane685@gmail.com

    + 💻 GitHub: @Vinhnub

    + 🌐 Project: Reddit Spam Detector