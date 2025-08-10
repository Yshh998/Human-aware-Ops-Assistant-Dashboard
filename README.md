# 🤖 Human-Aware Operations Assistant

A lightweight, human-centric web tool designed to help managers proactively identify employee overload and fatigue based on task data — with no logins, no setup, and no complexity.

---

## 🚀 Project Overview

Traditional task trackers miss the human cost of work. This tool helps managers see beyond output — surfacing real-time insights on who might be overworked, fatigued, or at risk of burnout.

Upload your team’s task data via CSV or Excel and instantly get:
- 📋 A snapshot of all task assignments
- ⚠️ Visual overload flags based on task duration and fatigue levels
- 📬 Simple feedback loop to capture usefulness of suggestions

---

## 🔧 How It Works

- Built using **Python** and **Streamlit**
- Accepts file uploads (`.csv` or `.xlsx`)
- Flags overload when:
  - **Task duration > 5 hours**
  - OR **Fatigue score ≥ 4** (on a 1–5 scale)
- Displays overload alerts and recommendations in a user-friendly interface

---

## 📂 Sample Columns (Your Data File Should Include)

| Column Name             | Example Value     |
|-------------------------|------------------|
| Employee Name           | John Doe          |
| Task Name               | Q2 Planning       |
| Task Duration (hrs)     | 6.5               |
| Fatigue Score (1–5)     | 4                 |

You can test with this [sample dataset of 100 employees](./employee_task_load_tracker_100.csv).

---

## 📈 Features

- ✅ Supports both `.csv` and `.xlsx` uploads
- ✅ Recommends reassignment for overloaded employees
- ✅ Gives managers immediate clarity into workload health
- ✅ Easy to use — no login or integrations required
- ✅ Includes feedback interaction for user insight
- ✅ **NEW:** Supports real-time file upload processing for instant results 

---

## 📅 Project Updates & Changelog

| Date       | Update Description |
|------------|--------------------|
| 2025-08-09 | AI-Powered Q&A Assistant added using Groq API for natural language insights on uploaded task data |
| 2025-08-05 | Enabled file uploads (CSV & Excel) instead of only Google Sheets link |
| 2025-08-03 | Initial overload detection prototype using Task Duration and Fatigue Score |

---

## 🔮 What’s Coming Next

- Predictive overload alerts using machine learning
- Integration with calendar and communication tools
- Configurable thresholds per department or role
- Dashboard for team-wide visibility
- Mobile-responsive version

---

## 💻 How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/yourusername/human-aware-ops-assistant.git
cd human-aware-ops-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

---

## 📄 File Structure

```
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── employee_task_load_tracker_100.csv  # Sample dataset
```

---

## 🙋‍♀️ Created By

**Vaishnavie Suresh**  
Operations & Product Manager | Human-Aware Systems Enthusiast  
🔗 [LinkedIn](https://www.linkedin.com/in/vaishnavie-suresh) | 🌐 [Portfolio](https://vaishnaviesuresh.theradarlist.com/)

---

## 📝 License

MIT License – free to use and modify.
