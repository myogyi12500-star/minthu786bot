# 🤖 Min Thu Bot V7 - Deployment Guide (အပြည့်အစုံ)

ဒီ guide မှာ @minthu786bot ကို အမြဲတမ်း 24/7 run နေအောင် deploy လုပ်နည်း step-by-step ပါဝင်ပါတယ်။

## လိုအပ်ချက်များ (Prerequisites)

Deploy မလုပ်ခင် ဒီအရာတွေ လိုအပ်ပါတယ်:

| Item | Description |
|------|-------------|
| **Bot Token** | Telegram BotFather ကနေ ရထားတဲ့ token |
| **Gemini API Key** | Google AI Studio (aistudio.google.com) ကနေ **အခမဲ့** ရယူနိုင်ပါတယ် |
| **GitHub Account** | Code ကို push ဖို့ (Railway/Render အတွက်) |

### Gemini API Key အခမဲ့ ရယူနည်း

1. https://aistudio.google.com/apikey သို့ သွားပါ
2. Google account နဲ့ login ဝင်ပါ
3. "Create API Key" ကို click ပါ
4. API key ကို copy ယူပါ - ဒါက `OPENAI_API_KEY` အဖြစ် သုံးပါမယ်

---

## နည်းလမ်း (1): Railway.app (အလွယ်ဆုံး - အကြံပြုပါတယ်)

Railway.app က GitHub repo ကနေ auto deploy လုပ်ပေးပါတယ်။ Credit card မလိုပါဘူး (trial credits ပေးပါတယ်)။

### Step 1: GitHub Repo ဖန်တီးပါ

1. https://github.com/new သို့ သွားပါ
2. Repository name: `minthu786bot`
3. "Create repository" click ပါ
4. Bot code files အားလုံးကို upload လုပ်ပါ:
   - `main.py`, `database.py`, `ai_features.py`, `features.py`
   - `requirements.txt`, `Procfile`, `Dockerfile`

**သို့မဟုတ် Git command line နဲ့:**
```bash
cd minthu786bot
git init
git add .
git commit -m "Initial commit - Min Thu Bot V7"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/minthu786bot.git
git push -u origin main
```

### Step 2: Railway.app မှာ Deploy လုပ်ပါ

1. https://railway.app/ သို့ သွားပါ
2. **"Login with GitHub"** click ပါ
3. Dashboard ထဲမှာ **"New Project"** click ပါ
4. **"Deploy from GitHub Repo"** ကို ရွေးပါ
5. `minthu786bot` repo ကို ရွေးပါ
6. Deploy စတင်ပါလိမ့်မယ်

### Step 3: Environment Variables ထည့်ပါ

Railway dashboard ထဲမှာ:
1. Project ကို click ပါ
2. **"Variables"** tab ကို click ပါ
3. ဒီ variables တွေ ထည့်ပါ:

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | `8101040719:AAGoEiSo7Mt4JNJpaAbj0Z91VyWeEMxEmYs` |
| `OPENAI_API_KEY` | သင့် Gemini API Key |
| `OPENAI_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` |

4. **"Deploy"** click ပါ - Bot run စပါလိမ့်မယ်!

---

## နည်းလမ်း (2): Render.com (အခမဲ့ - Credit card မလို)

Render.com မှာ free tier ရှိပြီး background worker အဖြစ် bot run နိုင်ပါတယ်။

### Step 1: GitHub Repo ဖန်တီးပါ (အထက်ပါ Step 1 အတိုင်း)

### Step 2: Render.com မှာ Deploy လုပ်ပါ

1. https://render.com/ သို့ သွားပါ
2. **"Get Started for Free"** click ပြီး GitHub နဲ့ sign up လုပ်ပါ
3. Dashboard ထဲမှာ **"New +"** → **"Background Worker"** ကို ရွေးပါ (Web Service မဟုတ်ပါ!)
4. GitHub repo `minthu786bot` ကို connect လုပ်ပါ
5. Settings:

| Setting | Value |
|---------|-------|
| Name | `minthu786bot` |
| Region | Singapore (အနီးဆုံး) |
| Branch | `main` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python main.py` |
| Plan | **Free** |

6. **Environment Variables** ထည့်ပါ:

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | `8101040719:AAGoEiSo7Mt4JNJpaAbj0Z91VyWeEMxEmYs` |
| `OPENAI_API_KEY` | သင့် Gemini API Key |
| `OPENAI_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` |

7. **"Create Background Worker"** click ပါ

> **မှတ်ချက်:** Render free tier မှာ 15 မိနစ် inactive ဖြစ်ရင် sleep ဝင်ပါတယ်။ Bot polling mode သုံးထားလို့ active ဖြစ်နေပါလိမ့်မယ်။

---

## နည်းလမ်း (3): Oracle Cloud Free Tier (အကောင်းဆုံး - အမြဲတမ်း အခမဲ့ VPS)

Oracle Cloud မှာ Always Free VPS server ရပါတယ်။ Credit card verify လိုပေမဲ့ charge မကျပါဘူး။

### Step 1: Oracle Cloud Account ဖွင့်ပါ

1. https://www.oracle.com/cloud/free/ သို့ သွားပါ
2. **"Start for free"** click ပါ
3. Account ဖွင့်ပါ (credit card verify လိုပါတယ် - charge မကျပါဘူး)

### Step 2: VM Instance ဖန်တီးပါ

1. OCI Console ထဲမှာ **Compute** → **Instances** → **Create Instance** click ပါ
2. Settings:

| Setting | Value |
|---------|-------|
| Name | `minthu786bot` |
| Image | Ubuntu 22.04 |
| Shape | VM.Standard.E2.1.Micro (Always Free) |
| | သို့မဟုတ် VM.Standard.A1.Flex (1 OCPU, 6GB RAM - Always Free) |
| Public IP | Assign public IPv4 address ✓ |
| SSH Key | Upload your SSH public key |

3. **"Create"** click ပါ

### Step 3: VM ထဲ ဝင်ပြီး Bot Install လုပ်ပါ

```bash
# SSH နဲ့ VM ထဲ ဝင်ပါ
ssh -i ~/.ssh/your_key ubuntu@YOUR_VM_PUBLIC_IP

# System update
sudo apt update && sudo apt upgrade -y

# Python install
sudo apt install python3 python3-pip git screen -y

# Bot code ယူပါ (GitHub repo ကနေ)
git clone https://github.com/YOUR_USERNAME/minthu786bot.git
cd minthu786bot

# Dependencies install
pip3 install -r requirements.txt

# Environment variables set (permanent)
echo 'export BOT_TOKEN="8101040719:AAGoEiSo7Mt4JNJpaAbj0Z91VyWeEMxEmYs"' >> ~/.bashrc
echo 'export OPENAI_API_KEY="YOUR_GEMINI_API_KEY"' >> ~/.bashrc
echo 'export OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"' >> ~/.bashrc
source ~/.bashrc
```

### Step 4: Bot ကို အမြဲတမ်း Run အောင် systemd service ဖန်တီးပါ

```bash
sudo nano /etc/systemd/system/minthu786bot.service
```

ဒီ content ကို paste ပါ:
```ini
[Unit]
Description=Min Thu Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/minthu786bot
Environment=BOT_TOKEN=8101040719:AAGoEiSo7Mt4JNJpaAbj0Z91VyWeEMxEmYs
Environment=OPENAI_API_KEY=YOUR_GEMINI_API_KEY
Environment=OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service enable & start
sudo systemctl daemon-reload
sudo systemctl enable minthu786bot
sudo systemctl start minthu786bot

# Status စစ်ရန်
sudo systemctl status minthu786bot

# Logs ကြည့်ရန်
sudo journalctl -u minthu786bot -f
```

> **ဒီနည်းက အကောင်းဆုံးပါ** - VM restart ဖြစ်ရင်တောင် bot auto start ပြန်လုပ်ပါတယ်။

---

## Troubleshooting

| ပြဿနာ | ဖြေရှင်းနည်း |
|---------|-------------|
| Bot reply မလုပ်ဘူး | BOT_TOKEN မှန်မမှန် စစ်ပါ |
| AI commands အလုပ်မလုပ်ဘူး | OPENAI_API_KEY နဲ့ OPENAI_BASE_URL စစ်ပါ |
| Duplicate detection အလုပ်မလုပ်ဘူး | Bot ကို group admin အဖြစ် ထည့်ထားမထား စစ်ပါ |
| Railway/Render deploy fail | Logs ကို စစ်ပါ - requirements install error ရှိနိုင်ပါတယ် |

---

## Files Structure

```
minthu786bot/
├── main.py           # Main bot entry point
├── database.py       # SQLite database functions
├── ai_features.py    # AI/Gemini powered commands
├── features.py       # All other feature commands
├── requirements.txt  # Python dependencies
├── Procfile          # Railway/Render process file
├── Dockerfile        # Docker container config
└── README.md         # Project documentation
```
