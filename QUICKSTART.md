# Quick Start - Run in 2 Minutes

## Install & Run

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Browser opens automatically at http://localhost:8501

## Try These 3 Demo Scenarios

### 1. Auto-Resolution (Simple Request)
1. In sidebar, select: **"REQ-02: Vikram Chawla"**
2. Click **"Load Request"**
3. Click **"Submit Request"**
4. ✅ See: Instant resolution with KB-07 citation

### 2. Policy Conflict Detection
1. Select: **"REQ-01: Aditi Sharma"**
2. Click **"Load Request"** → **"Submit Request"**
3. ⚠️ See: Conflict between KB-03 (3 years) and Asset Policy (4 years)

### 3. Security Escalation
1. Select: **"REQ-08: Ananya Reddy"**
2. Click **"Load Request"** → **"Submit Request"**
3. 🚨 See: URGENT escalation + warning about forwarding violation

## Explore Features

- **Ticket Queue Tab**: View all tickets created
- **Audit Trail Tab**: See complete decision logs
- **Custom Requests**: Enter your own IT support requests

## Test All 15 Scenarios

```powershell
python tests\test_scenarios.py
```

Validates all employee requests from the assignment.

---

**Need Help?** See `SETUP.md` for troubleshooting or `README.md` for full documentation.
