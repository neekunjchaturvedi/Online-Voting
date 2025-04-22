# Online Voting System

Welcome to the **Online Voting System**! This project is a simple and secure online voting application built using Python, Streamlit, and SQLAlchemy.

## Features

- **User Authentication**: 
  - Login and registration functionalities are handled in `auth.py`.
  - Ensures secure access to the platform using local database storage.

- **Voting Mechanism**:
  - Core voting logic is implemented in `voting.py`.
  - Handles vote submissions and prevents duplicate votes.

- **User-Friendly Interface**:
  - Built with Streamlit for an interactive and responsive user experience.
  - The interface resides in `main.py`.

- **Local Database Handling**:
  - SQLAlchemy is used to manage the local database efficiently.
  - Handles user data, voting records, and other persistent data.

## How to Run the Project

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or later
- Streamlit library
- SQLAlchemy library

Install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/neekunjchaturvedi/Online-Voting.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Online-Voting
   ```
3. Start the application:
   ```bash
   streamlit run main.py
   ```

The application will open in your default web browser.

## File Structure

- `auth.py`: Contains the authentication logic for login and registration, integrated with SQLAlchemy for database handling.
- `voting.py`: Implements the voting logic, including vote validation and tallying, with database support.
- `main.py`: The Streamlit-based user interface for the application.
- `requirements.txt`: List of dependencies required to run the project.

## Database Handling

This project uses **SQLAlchemy** as the Object-Relational Mapper (ORM) to handle the local database. It is used to:

- Store user credentials securely.
- Manage voting data, ensuring data integrity.
- Provide an easy-to-use interface for database interactions.

## Screenshots

*(Add screenshots or GIFs of your application here to make it visually appealing.)*

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
