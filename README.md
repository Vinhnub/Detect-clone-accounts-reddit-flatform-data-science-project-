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

├── 📁 .github
│   └── 📁 workflows
│       └── ⚙️ auto.yml
├── 📁 crawReditRender
│   ├── 📁 data
│   │   └── ⚙️ .gitkeep
│   ├── 📝 README.md
│   ├── 🐍 app.py
│   ├── 🐍 reddit_crawler.py
│   └── 📄 requirements.txt
├── 📁 data_prepare
│   ├── 📁 Huy
│   │   ├── 🖼️ heat_map_activate_comment.png
│   │   ├── 🖼️ heat_map_activate_post.png
│   │   ├── 🐍 heatmap_activate_week_post_comment.py.py
│   │   ├── 🖼️ scatter_post_link_karma.png
│   │   └── 🐍 scratter_postScore_karma.py.py
│   ├── 📁 Kiet
│   │   ├── 🖼️ Figure_1.png
│   │   ├── 🖼️ Figure_2.png
│   │   ├── 🐍 Verified_and_Premium_rate.py
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 account_created_chart.py
│   ├── 📁 Trung
│   │   ├── 🖼️ Figure_1.png
│   │   ├── 🖼️ Figure_2.png
│   │   ├── 🖼️ Figure_3.png
│   │   └── 🐍 Lab.py
│   ├── 📁 Vinh
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 correlation_comment_and_post_karma.py
│   │   ├── 🖼️ distribute_comment_duplicate_score.png
│   │   ├── 🖼️ distribute_post_duplicate_score.png
│   │   ├── 🐍 duplicate_ratio_calculate.py
│   │   ├── 📄 duplicate_score.csv
│   │   ├── 🖼️ duplicate_score_distribute_plot.png
│   │   ├── 🐍 duplicate_statistic.py
│   │   ├── 📄 duplicate_statistic.txt
│   │   ├── 🖼️ relationship_comment_and_post_karma.png
│   │   └── 🖼️ relationship_post_and_comment_duplicate_score.png
│   └── 📁 viewUserDuplicates
│       ├── 🖼️ result.png
│       └── 🐍 viewUserDuplicates.py
├── 📁 database
│   ├── 📁 data
│   ├── 📁 image
│   │   ├── 🖼️ ERD.png
│   │   └── 🖼️ diagram.png
│   ├── 📁 new_data
│   ├── 🐍 __init__.py
│   ├── 🐍 data_mixer.py
│   ├── 🐍 database_access.py
│   ├── 🐍 database_fetcher.py
│   └── 📄 query.sql
├── 📁 get_data
│   ├── 🐍 __init__.py
│   ├── 🐍 constants.py
│   ├── 🐍 reddit_crawler.py
│   └── 🐍 reddit_crawler_to_sqlite.py
├── 📁 utils
│   └── 🐍 __init__.py
├── ⚙️ .gitignore
├── 📘 ContentLAB_4_5.docx
├── 📝 README.md
├── 🐍 auth.py
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
