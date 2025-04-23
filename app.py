import cv2
import streamlit as st
import requests
import datetime
from ultralytics import YOLO
from ultralytics.utils import LOGGER

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_BOT_CHAT_ID"


class Inference:
    def __init__(self):
        """Initializes the Inference class, setting up the model path and UI."""
        self.st = st
        self.source = None  # Video or webcam source
        self.enable_trk = False  # Object tracking flag
        self.conf = 0.25  # Confidence threshold
        self.iou = 0.45  # IoU threshold
        self.org_frame = None  # Original frame
        self.ann_frame = None  # Annotated frame
        self.vid_file_name = None  # Video filename
        self.selected_ind = []  # Selected classes
        self.model = None  # YOLO model instance
        self.stop_flag = False  # Stop button flag
        self.available_models = {"wildv8": "wild8.pt", "wild11": "wild11.pt"}

        LOGGER.info("✅ Wildlife Detection Initialized!")

    def web_ui(self):
        """Sets up the Streamlit web interface."""
        self.st.set_page_config(page_title="Wildlife Conservation App", layout="wide")
        self.st.markdown(
            "<h1 style='text-align:center; color:#900C3F;'>🌿 Wildlife Conservation & Poaching Prevention 🦌🔍</h1>",
            unsafe_allow_html=True
        )
        self.st.markdown(
            "<h4 style='text-align:center; color:#a4530b;'>Experience Real-Time Object Detection for Wildlife Protection 🌎🚨</h4>",
            unsafe_allow_html=True
        )

    def sidebar(self):
        """Configures the Streamlit sidebar for user settings."""
        with self.st.sidebar:
            self.st.image("image.png", width=250)

        self.st.sidebar.title("🔧 User Configuration")
        self.source = self.st.sidebar.selectbox("📹 Video Source", ("webcam", "video"))
        self.enable_trk = self.st.sidebar.radio("🎯 Enable Tracking?", ("Yes", "No"))
        self.conf = self.st.sidebar.slider("⚙️ Confidence Threshold", 0.0, 1.0, self.conf, 0.01)
        self.iou = self.st.sidebar.slider("⚙️ IoU Threshold", 0.0, 1.0, self.iou, 0.01)

        col1, col2 = self.st.columns(2)
        self.org_frame = col1.empty()
        self.ann_frame = col2.empty()

    def source_upload(self):
        """Handles video file uploads."""
        self.vid_file_name = ""
        if self.source == "video":
            vid_file = self.st.sidebar.file_uploader("📂 Upload Video File", type=["mp4", "mov", "avi", "mkv"])
            if vid_file is not None:
                with open("wildlife_video.mp4", "wb") as out:
                    out.write(vid_file.read())
                self.vid_file_name = "wildlife_video.mp4"
        elif self.source == "webcam":
            self.vid_file_name = 0  # Webcam source

    def configure(self):
        """Configures and loads the selected model."""
        self.st.sidebar.title("🛠️ Model Selection")

        use_wild11 = self.st.sidebar.checkbox("🐅 WILD 11", value=True)
        use_wild8 = self.st.sidebar.checkbox("🐆 WILD 8", value=False)

        if use_wild11 and use_wild8:
            self.st.warning("⚠️ Select only one model at a time!")
            return

        selected_model = "wild11" if use_wild11 else "wildv8"

        with self.st.spinner(f"🔄 Loading {selected_model}.pt model..."):
            model_path = self.available_models[selected_model]
            self.model = YOLO(model_path)  # Load YOLO model
            class_names = list(self.model.names.values())

        self.st.success(f"✅ Model {selected_model}.pt loaded successfully!")

        # Class selection
        selected_classes = self.st.sidebar.multiselect("🎭 Select Classes", class_names, default=class_names[:3])
        self.selected_ind = [class_names.index(option) for option in selected_classes]

    def send_telegram_alert(self, message, frame):
        """Sends a Telegram alert with an image when a hunter and an animal are detected."""
        image_path = "detected_frame.jpg"

        # 🕒 Add timestamp and alert message to the image
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Define text size
        (text_width, text_height), baseline = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)

        # Define text position
        text_x, text_y = 10, 60  # Position for timestamp
        alert_position = (10, 30)  # Position for "Alert"

        # Draw a white rectangle behind text (Adjusted size)
        cv2.rectangle(frame, (text_x, text_y - text_height - 5),
                      (text_x + text_width, text_y + 5), (255, 255, 255), -1)

        # Draw Alert text (small font, red)
        cv2.putText(frame, "Alert", alert_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Put timestamp text over white rectangle
        cv2.putText(frame, timestamp, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        # Save the image
        cv2.imwrite(image_path, frame)

        # Send alert message
        url_message = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data_message = {"chat_id": CHAT_ID, "text": message}
        requests.post(url_message, data=data_message)

        # Send image
        url_photo = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as image_file:
            requests.post(url_photo, data={"chat_id": CHAT_ID}, files={"photo": image_file})

        print("📸 Image sent to Telegram with timestamp and alert message!")

    def inference(self):
        """Runs object detection inference."""
        self.web_ui()
        self.sidebar()
        self.source_upload()
        self.configure()

        start_button = self.st.sidebar.button("🚀 Start")
        stop_button = self.st.sidebar.button("⏹️ Stop")

        if start_button:
            cap = cv2.VideoCapture(self.vid_file_name)
            self.stop_flag = False  # Reset stop flag

            if not cap.isOpened():
                self.st.error("❌ Could not open video source.")
                return

            while cap.isOpened():
                if self.stop_flag:
                    break  # Stop loop when Stop button is clicked

                success, frame = cap.read()
                if not success:
                    self.st.warning("⚠️ Failed to read frame from source.")
                    break

                results = self.model(frame, conf=self.conf, iou=self.iou, classes=self.selected_ind)
                annotated_frame = results[0].plot()

                detected_classes = {self.model.names[int(det.cls)] for det in results[0].boxes}

                if "hunter" in detected_classes and "animal" in detected_classes:
                    self.send_telegram_alert("🚨 Urgent Alert! Hunter detected near wildlife!", annotated_frame)

                self.org_frame.image(frame, channels="BGR")
                self.ann_frame.image(annotated_frame, channels="BGR")

            cap.release()
        cv2.destroyAllWindows()

        if stop_button:
            self.stop_flag = True  # Set stop flag when Stop button is clicked


if __name__ == "__main__":
    Inference().inference()
