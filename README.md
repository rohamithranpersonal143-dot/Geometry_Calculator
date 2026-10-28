# 📐 OmniMath Engine

An interactive, high-precision geometry analytics dashboard built using Python and Streamlit. **OmniMath Engine** offers instant multi-dimensional calculations for 2D surfaces and 3D spatial solids within a unified, responsive web interface.

## ✨ Key Features
- **Dual Workspace Architecture:** Toggle seamlessly between 2D Shape Analytics (perimeter/area) and 3D Spatial Volumetrics.
- **Dynamic Scale Profiles:** Built-in runtime unit transformations supporting metric (`m`, `cm`), imperial (`in`, `ft`), or user-defined custom settings.
- **Robust Math Solvers:** Advanced computing logic to safely handle trigonometric profiles, interior angles, and multi-sided custom regular polygons without domain errors.
- **Responsive Metrics UI:** Streamlit grid components optimized for beautiful visualization across devices.

## 📁 Repository Directory Map
```text
omnimath-engine/
├── .gitignore          # Filters system clutter (venv/, __pycache__/)
├── LICENSE            # Open-source permissions (MIT)
├── README.md          # Project overview & deployment documentation
├── requirements.txt   # Web framework dependencies configurations
└── main.py            # Primary application UI layout entrypoint
```

## 🚀 Local Installation & Deployment

Follow these quick commands to spin up the workspace engine on your machine:

1. **Clone the repository container:**
   ```bash
   git clone https://github.com
   cd omnimath-engine
   ```

2. **Initialize your dependencies profile:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit dashboard:**
   ```bash
   streamlit run main.py
   ```

## 🛠️ Built With
- **Python 3** - Core structural algorithms and pure math logic (`math`).
- **Streamlit** - High-speed interactive UI rendering framework.
