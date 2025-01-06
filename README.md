# YouTube Sponsorship Detector

This project is designed to detect sponsorships in YouTube video descriptions. It uses the YouTube Data API to fetch video details and processes the descriptions to identify sponsorships.

## Project Structure

- `app.py`: Contains the Flask application with endpoints for detecting publications and confirming channel subscriptions.
- `youtube.py`: Contains the `YouTubeAPI` class for interacting with the YouTube Data API.
- `dataclass/Publication.py`: Contains the `Publication` data class for handling YouTube publication data.
- `dataclass/detector.py`: Contains the `YoutubeSponsorshipDetector` class for processing and detecting sponsorships.


## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/munir-moh/youtube_sponsorship_detector.git
    cd youtube_sponsorship_detector
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file  and set your YouTube API key:
    

5. Set your YouTube API key in the `.env` file:
    ```dotenv
    YOUTUBE_API_KEY=your_youtube_api_key_here
    ```

## Running the Application

1. Start the Flask application:
    ```bash
    python app.py
    ```

2. The application will be available at `http://127.0.0.1:5000`.

## Endpoints

- `GET /`: Home endpoint that triggers the `YoutubeSponsorshipDetector`.
- `GET /channels`: Endpoint to confirm channel subscription.
- `POST /channels`: Endpoint to detect publication and process the description.
- `GET /youtube-publications`: Endpoint to fetch YouTube video details by publication IDs.

## Example Usage

To detect sponsorships in a YouTube video description, send a POST request to the `/channels` endpoint with the XML data of the publication.

```bash
curl -X POST http://127.0.0.1:5000/channels -d @publication.xml
```

## License

This project is licensed under the MIT License.
