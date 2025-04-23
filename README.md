Here’s your updated **README.md** with a section to display images (such as screenshots or output examples) after the `app.py` line for better project visualization:

---

# 🦌 Wildlife Detection & Poaching Prevention System

An **AI & IoT-based real-time wildlife monitoring system** developed using **YOLOv8/YOLOv11**, powered by the **Seeed Studio J1010 Jetson Nano** and integrated with a **Telegram alert system** for instant poaching detection notifications.

---

## 🔍 Features
- 🎯 Real-time object detection (Animals, Hunters, Humans)  
- 🚨 Telegram alert system for poaching threats  
- 📹 Video input support (pre-recorded & live)  
- ⚡ Edge AI processing using Jetson Nano  
- 📊 Interactive Streamlit dashboard for visualization  

---

## 🛠️ Tech Stack
- **YOLOv8 / YOLOv11** – Object detection models (Ultralytics)  
- **Jetson Nano J1010** – Edge AI hardware  
- **OpenCV** – Video frame handling  
- **Roboflow** – Dataset annotation & preprocessing  
- **Streamlit** – Web-based dashboard  
- **Telegram Bot API** – Real-time alerts  
- **Google Colab** – Model training environment  

---

## 🚀 Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Joe-KI333/jetson-nano-wildlife-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your Telegram Bot token and chat ID in `config.py`.  
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## 🖼️ Output Screenshots

### 🔹 Streamlit Dashboard
![Dashboard](https://github.com/user-attachments/assets/1a97ecb3-cbe4-4fd3-8fd2-52b5c8f07f1c)

### 🔹 Telegram Alert
![Telegram Alert](![TelegramBot](https://github.com/user-attachments/assets/2e51beb6-abb4-4d3e-8753-4d97d73faeb5)


### 🔹 Detection Output
![YOLO Detection](![Webcamv8](https://github.com/user-attachments/assets/718e6de6-af05-49ab-b0fe-0ef09ecc5246) ![Video11](https://github.com/user-attachments/assets/57e01fb0-8fa3-430c-a5c1-45af7f8fe549)
![terminal](https://github.com/user-attachments/assets/97c463c5-2a81-4909-8c8c-9872541256e9)


## 📁 Dataset
Annotated using **Roboflow** with 3 classes:
- Animal  
- Hunter  
- Human  

---

## 🤝 Credits
Developed by **Joel** & **Simran**  

---

## 🌍 Let’s Make a Difference
This project is designed to help **conservationists** and **forest departments** monitor wildlife and prevent poaching through the power of **AI** and **Edge Computing**.

---

## 📬 Contact
Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/joelnadar123/) for queries, collaborations, or feedback!
