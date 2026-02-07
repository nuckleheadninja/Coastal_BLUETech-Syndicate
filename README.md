# 🌊 Coastal Pollution Monitor

> **AI-Powered Coastal Protection Platform**  
> *Protecting our oceans through intelligent detection, real-time mapping, and community action.*

![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![React](https://img.shields.io/badge/react-18-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-teal.svg)
![CLIP](https://img.shields.io/badge/AI-CLIP%20Vision-purple.svg)
![SQLite](https://img.shields.io/badge/database-SQLite-orange.svg)

---

## 🌟 Overview

The **Coastal Pollution Monitor** is a full-stack web application that empowers citizens and organizations to fight marine pollution. Using **OpenAI's CLIP model** for zero-shot image classification, it transforms photos into actionable data points on a live map, enabling rapid response from environmental NGOs.

### 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **AI Classification** | CLIP-based detection of 5 categories: Plastic, Oil Spill, Solid Waste, Marine Debris, No Waste |
| 📍 **GPS Auto-Extract** | Automatically extracts location from image EXIF data or browser geolocation |
| 🗺️ **Live Map** | Real-time visualization of pollution hotspots with filtering |
| 👤 **User System** | Complete authentication with signup, login, and role-based access |
| 🛡️ **Admin Dashboard** | Manage reports, forward to NGOs, mark as resolved |
| 🤝 **NGO Integration** | Partner directory with report forwarding capability |
| ✅ **False Detection Filter** | "No Waste" category prevents false positives |

---

## 🎨 Application Pages

### Public Pages
| Page | Route | Description |
|------|-------|-------------|
| 🏠 **Home** | `/` | Landing page with hero section, live stats, and workflow visualization |
| 🗺️ **Map** | `/map` | Interactive Leaflet map with pollution markers and filtering |
| 🤝 **NGOs** | `/ngos` | Partner organization directory with search |

### Authentication
| Page | Route | Description |
|------|-------|-------------|
| 🔐 **Login** | `/login` | User authentication with JWT tokens |
| 📝 **Signup** | `/signup` | New user registration |

### Protected Pages (Requires Login)
| Page | Route | Description |
|------|-------|-------------|
| 📸 **Upload Report** | `/upload` | Submit pollution photos with AI analysis |
| 👤 **Profile** | `/profile` | View user's submitted reports |

### Admin Only
| Page | Route | Description |
|------|-------|-------------|
| 🛡️ **Admin Dashboard** | `/admin` | Manage all reports, users, forward to NGOs |

---

## 🏗️ Project Structure

```
coastal-pollution-monitor/
│
├── 📁 backend/
│   ├── main.py              # FastAPI app, all API endpoints
│   ├── ml_model.py          # CLIP AI classification logic
│   ├── database.py          # SQLite operations & schema
│   ├── auth.py              # JWT authentication & password hashing
│   ├── requirements.txt     # Python dependencies
│   ├── test_data.py         # Generate sample pollution data
│   ├── pollution.db         # SQLite database (auto-created)
│   └── 📁 uploads/          # Uploaded images storage
│
├── 📁 frontend/
│   ├── 📁 public/
│   │   └── index.html       # HTML template
│   ├── 📁 src/
│   │   ├── App.js           # React Router configuration
│   │   ├── index.js         # React entry point
│   │   ├── index.css        # Global styles (glassmorphism theme)
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── Navbar.jsx       # Navigation bar
│   │   │   ├── OceanWaves.jsx   # Animated background
│   │   │   └── ProtectedRoute.jsx # Auth route wrapper
│   │   │
│   │   ├── 📁 context/
│   │   │   └── AuthContext.js   # Authentication state management
│   │   │
│   │   └── 📁 pages/
│   │       ├── Home.jsx         # Landing page
│   │       ├── Map.jsx          # Interactive pollution map
│   │       ├── Upload.jsx       # Report submission
│   │       ├── NGOs.jsx         # NGO partner directory
│   │       ├── Login.jsx        # User login
│   │       ├── Signup.jsx       # User registration
│   │       ├── Profile.jsx      # User profile & reports
│   │       └── AdminDashboard.jsx # Admin control panel
│   │
│   └── package.json         # Node.js dependencies
│
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── API.md                   # API documentation
├── SETUP.md                 # Detailed setup guide
└── README.md                # This file
```

---

## 🧠 AI Classification Categories

The CLIP model classifies images into 5 categories:

| Category | Icon | Description | Confidence Threshold |
|----------|------|-------------|---------------------|
| 🥤 **Plastic** | `#ef4444` (Red) | Plastic bottles, bags, wrappers | >85% |
| 🛢️ **Oil Spill** | `#1f2937` (Dark) | Petroleum contamination, dark murky water | >85% |
| 🗑️ **Solid Waste** | `#92400e` (Brown) | Garbage piles, trash on beach | >85% |
| 🎣 **Marine Debris** | `#0ea5e9` (Blue) | Fishing nets, ropes, buoys | >85% |
| ✅ **No Waste** | `#22c55e` (Green) | Clean water, no pollution detected | Default fallback |

> **Note**: If confidence is below 85%, the system defaults to "No Waste" to prevent false positives.

---

## ⚡ Quick Start

### Prerequisites
- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)

### 1️⃣ Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

🟢 **Backend runs at**: `http://localhost:8000`

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

🟢 **Frontend runs at**: `http://localhost:3000`

### 3️⃣ Default Admin Account

After starting the backend, a default admin is created:

| Field | Value |
|-------|-------|
| Email | `admin@coastal.com` |
| Password | `admin123` |

### 4️⃣ Generate Test Data (Optional)

```bash
cd backend
python test_data.py
```

This creates sample pollution reports with images for testing.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/signup` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login & get JWT token | ❌ |
| `GET` | `/api/reports` | Get all public reports | ❌ |
| `GET` | `/api/stats` | Get pollution statistics | ❌ |
| `GET` | `/api/ngos` | List partner NGOs | ❌ |
| `POST` | `/api/upload` | Submit pollution report | ✅ |
| `POST` | `/api/extract-gps` | Extract GPS from image | ❌ |
| `GET` | `/api/user/reports` | Get user's reports | ✅ |
| `GET` | `/api/admin/reports` | Get all reports (admin) | ✅ Admin |
| `PUT` | `/api/admin/reports/{id}` | Update report status | ✅ Admin |

> See `API.md` for detailed documentation.

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async API framework |
| **CLIP (OpenAI)** | Zero-shot image classification |
| **SQLite** | Lightweight database |
| **JWT** | Token-based authentication |
| **bcrypt** | Secure password hashing |
| **Pillow** | Image processing & EXIF extraction |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **React Router v6** | Client-side routing |
| **Leaflet.js** | Interactive maps |
| **Axios** | HTTP client |
| **jwt-decode** | Token parsing |
| **CSS3** | Glassmorphism styling |

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Backend
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

---

## 📱 Screenshots

### Home Page
- Hero section with animated ocean waves
- Live statistics dashboard
- Step-by-step workflow guide

### Upload & AI Analysis
- Camera/Gallery upload options
- Automatic GPS extraction
- Real-time AI classification results

### Interactive Map
- Color-coded pollution markers
- Filter by pollution type
- Rich popups with report details

### Admin Dashboard
- Report management table
- Status updates (Pending → Forwarded → Resolved)
- User management

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **OpenAI CLIP** - Zero-shot image classification
- **Leaflet.js** - Beautiful interactive maps
- **FastAPI** - Modern Python web framework
- **React** - Frontend UI library

---

**Made with 💙 for Cleaner Oceans**  
*Empowering communities to protect our coastlines*
