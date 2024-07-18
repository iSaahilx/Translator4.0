import React from 'react';
import Translator from './components/Translator';
import './App.css'; // Import CSS file for styling

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Language Translator</h1>
            </header>
            <main>
                <Translator />
            </main>
            <footer className="App-footer">
                <p>&copy; 2024 Translator App</p>
            </footer>
        </div>
    );
};

export default App;
