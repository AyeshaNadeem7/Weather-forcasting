🌤️ Weather Broadcast

A professional, responsive weather dashboard built with Python and Streamlit, using the OpenWeather API to provide real-time weather information for major cities across Pakistan.

✨ Features

🌍 Real-time weather information

🇵🇰 15 Pakistani cities

📍 Rawalpindi selected by default

🔄 Dynamic city selection

🌡️ Current temperature

🤒 Feels-like temperature

💧 Humidity

💨 Wind speed and direction

☁️ Cloud coverage

📊 Atmospheric pressure

👁️ Visibility

🌅 Sunrise and sunset times

🌧️ Rain probability

📝 Automatic weather summary

🔄 Refresh weather button

📱 Responsive professional interface

🌙 Modern dark-themed dashboard

🔐 API key stored separately from the source code

🛠️ Technologies Used

Python
Streamlit
Requests
OpenWeather API

📁 Project Structure

weather-broadcast/
│
├── app.py

├── test-api.py

├── requirements.txt

├── README.md

├── .gitignore

├── api_key.txt          # Keep private - DO NOT upload

└── .venv/               # Local virtual environment - DO NOT upload

🔑 OpenWeather API Key

This project uses the OpenWeather API.

Create an account on OpenWeather and generate an API key.

Store your API key in a file named:

api_key.txt

The file should contain only your API key:

YOUR_OPENWEATHER_API_KEY

Do not add quotes or extra text.

Windows:

2. python -m venv .venv

3. Activate the virtual environment
   
.venv\Scripts\Activate.ps1

5. Install dependencies
   
pip install -r requirements.txt

7. Add your API key

Create: api_key.txt

and put your OpenWeather API key inside it.

6. Run the application
   
streamlit run app.py

The application will open in your browser.

🏙️ Supported Cities

The dashboard currently supports:

Rawalpindi
Islamabad
Lahore
Karachi
Peshawar
Quetta
Multan
Faisalabad
Gujranwala
Sialkot
Hyderabad
Bahawalpur
Sargodha
Abbottabad
Mardan

📄 License

This project is available for educational and personal use.

👨‍💻 Author

Built as a Python + Streamlit weather dashboard project.

Weather Broadcast 🌤️
Live weather intelligence for Pakistan
