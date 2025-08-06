# To-Do List Application

This is a simple To-Do List application built using HTML and styled with Tailwind CSS. The application allows users to add and remove tasks, providing a clean and user-friendly interface.

## Project Structure

```
todo-list-app
├── src
│   ├── todo.html          # HTML structure for the To-Do List application
│   └── styles
│       └── tailwind.css   # Tailwind CSS styles with a pastel color theme
├── package.json           # npm configuration file
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd todo-list-app
   ```

2. **Install dependencies:**
   Make sure you have Node.js installed. Then run:
   ```bash
   npm install
   ```

3. **Build Tailwind CSS:**
   To generate the Tailwind CSS file, run:
   ```bash
   npx tailwindcss -i ./src/styles/tailwind.css -o ./dist/output.css --watch
   ```

4. **Open the application:**
   Open `src/todo.html` in your web browser to view the To-Do List application.

## Usage

- Add a new task by typing in the input field and clicking the "추가" button.
- Remove a task by clicking the "삭제" button next to the task.

## License

This project is open-source and available under the [MIT License](LICENSE).