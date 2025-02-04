from PySide6.QtWidgets import *
from PySide6 import QtCore
import requests
from widgets.functions.gpt_interface import get_gpt_response

class APITab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout setup
        self.layout = QGridLayout(self)

        # Scroll area setup
        self.tab_scroll_area = QScrollArea(self)
        self.tab_scroll_area.setWidgetResizable(True)
        self.tab_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.layout.addWidget(self.tab_scroll_area)

        # Frame setup inside the scroll area
        self.api_frame = QFrame(self)
        self.api_frame.setProperty("class", "frame-background")
        self.api_frame.setLayout(QVBoxLayout())
        self.tab_scroll_area.setWidget(self.api_frame)

        # Define farming data variables and their units (8 fields as per your request)
        self.farming_data = [
            ("Temperature", "°F", QLineEdit()),
            ("Humidity", "%", QLineEdit()),
            ("Precipitation", "in", QLineEdit()),
            ("UV Index", "", QLineEdit()),
            ("Wind Speed", "mph", QLineEdit()),
            ("Pressure", "in", QLineEdit()),
            ("Dewpoint", "°F", QLineEdit()),
            ("Cloud Cover", "%", QLineEdit())
        ]

        # Adding widgets in grid layout (with labels on the same line as inputs)
        for i, (title, unit, input_box) in enumerate(self.farming_data):
            row_layout = QHBoxLayout()  # Horizontal layout for label and input box
            label = QLabel(f"{title} ({unit})" if unit else title)
            label.setAlignment(QtCore.Qt.AlignLeft)

            # Styling the label and input box
            label.setStyleSheet("font-size: 22px; padding-right: 10px;")
            label.setFixedWidth(300)  # Set fixed width for all labels
            input_box.setStyleSheet("font: black; padding: 10px; padding-right: 20px; font-size: 14px; "
                                    "border-radius: 5px; background-color: rgb(70, 120, 110); color: white;")  # Set background color

            row_layout.addWidget(label)
            row_layout.addWidget(input_box)

            # Add the row to the main frame
            self.api_frame.layout().addLayout(row_layout)

        # Add autofill button for fetching weather data based on user location
        self.autofill_button = QPushButton("Use API to Autofill Based On Your Location")
        self.autofill_button.setStyleSheet("background-color: rgb(70, 120, 110); color: white; padding: 8px; border-radius: 5px;"
                                           "QPushButton:hover { background-color: rgb(90, 150, 140); }")
        self.api_frame.layout().addWidget(self.autofill_button)

        # Adding Run button at the bottom
        self.run_button = QPushButton("Run")
        self.run_button.setStyleSheet("background-color: rgb(70, 120, 110); color: white; padding: 8px; border-radius: 5px;"
                                      "QPushButton:hover { background-color: rgb(90, 150, 140); }")
        self.api_frame.layout().addWidget(self.run_button)

        # Ensuring layout has enough space (no bottom padding)
        self.api_frame.layout().setContentsMargins(20, 10, 20, 0)  # No bottom padding
        self.api_frame.layout().setSpacing(30)

        # Connect the run button to trigger the API call
        self.run_button.clicked.connect(self.trigger_gpt_response)

        # Connect autofill button to fetch weather data
        self.autofill_button.clicked.connect(self.fetch_weather_data)

    def fetch_weather_data(self):
        # Fetching the user's IP-based location (using a simple IP geolocation service)
        ip_info_url = "http://ip-api.com/json"
        ip_response = requests.get(ip_info_url)
        location_data = ip_response.json()

        # Extracting city from the IP geolocation API response
        city = location_data.get('city', 'London')  # Defaulting to London if location is not found

        # Weather API key (replace with your actual key)
        API_KEY = "197063ef56bb420599873502252801"
        
        # Fetching weather data based on location
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        # Fetching the required data from the Weather API response
        temp_f = weather_data['current']['temp_f']
        humidity = weather_data['current']['humidity']
        precip_in = weather_data['current']['precip_in']
        uv = weather_data['current']['uv']
        wind_mph = weather_data['current']['wind_mph']
        pressure_in = weather_data['current']['pressure_in']
        dewpoint_f = weather_data['current']['dewpoint_f']
        cloud = weather_data['current']['cloud']

        # Updating the UI with the fetched weather data
        self.farming_data[0][2].setText(f"{temp_f} °F")  # Temperature
        self.farming_data[1][2].setText(f"{humidity} %")  # Humidity
        self.farming_data[2][2].setText(f"{precip_in} in")  # Precipitation
        self.farming_data[3][2].setText(f"{uv}")  # UV Index
        self.farming_data[4][2].setText(f"{wind_mph} mph")  # Wind Speed
        self.farming_data[5][2].setText(f"{pressure_in} in")  # Pressure
        self.farming_data[6][2].setText(f"{dewpoint_f} °F")  # Dewpoint
        self.farming_data[7][2].setText(f"{cloud} %")  # Cloud Cover

    def trigger_gpt_response(self):
        # Gather the values from the input fields
        api_inputs = [input_box.text() for _, _, input_box in self.farming_data]

        # Extract the city and country from the IP location data
        city = self.farming_data[0][2].text()  # Assuming city info is already set in the first field (Temperature)
        country = self.farming_data[1][2].text()  # Similarly assuming you have country info

        # Create the concise prompt for GPT
        prompt = (f"Given the following weather conditions in {city}, {country}: "
                f"Temperature: {api_inputs[0]}, Humidity: {api_inputs[1]}, Precipitation: {api_inputs[2]}, "
                f"UV Index: {api_inputs[3]}, Wind Speed: {api_inputs[4]}, Pressure: {api_inputs[5]}, "
                f"Dewpoint: {api_inputs[6]}, Cloud Cover: {api_inputs[7]}, "
                f"Please tell me the amount of water to provide for the crops in mL and in what intervals under these conditions. Use good sources so that even if I ask you same thing again, you are consistently accurate with your responses.")

        # Call the GPT function with the prompt
        response = get_gpt_response(prompt, self.farming_data, 1500, api_inputs)

        # Display the response in a popup (QMessageBox)
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("GPT Response")
        msg_box.setText(response)  # Set the response as the message
        msg_box.setStandardButtons(QMessageBox.Ok)  # Only OK button
        msg_box.exec()  # Show the popup