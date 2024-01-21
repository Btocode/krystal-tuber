# KrystalTuber - Youtube Video Downloader and Audio Converter

A Flask backend application to download YouTube videos and convert them to audio. This project makes it easy to handle YouTube URLs for both downloading and extracting audio, with a focus on simplicity and efficiency.

## Features

- **Download YouTube Videos**: Allows downloading videos directly from YouTube URLs.
- **Convert Videos to Audio**: Extracts and converts YouTube videos into audio files.
- **Development with Hot Reloading**: Utilizes Flask's hot reloading feature for a smoother development experience.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3
- Flask

### Installing

A step by step series of examples that tell you how to get a development environment running.

1. **Clone the Repository**

   ```
   git clone https://github.com/Btocode/krystal-tuber.git
   cd krystal-tuber
   ```
2. **Install Dependencies**

   ```
   pip install -r requirements.txt
   ```

### Running the Application

For development, you can run the project with hot reloading enabled:

```bash
flask --app run.py --debug run
```

This will start the Flask server in development mode with hot reloading.

## Additional Commands

- **Production Mode**:

  ```
  flask --app run.py run
  ```

  *Note: Make sure to set `FLASK_ENV` to `production` when running in a production environment.*
- **Testing**:
  *Include instructions for running any tests that you have for your project.*

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **S Afsan Rahmatullah** - *Initial work* - [BTOCODE](https://github.com/Btocode "Afsan")

## License

This project is licensed under the [License Name] License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
