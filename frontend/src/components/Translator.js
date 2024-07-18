import React, { useState } from 'react';
import axios from 'axios';

const Translator = () => {
    const [text, setText] = useState('');
    const [targetLanguage, setTargetLanguage] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [audioUrl, setAudioUrl] = useState('');

    const handleTranslate = async () => {
        try {
            const response = await axios.post('http://localhost:5000/translate', {
                text: text,
                target_language: targetLanguage,
            });
            setTranslatedText(response.data.translated_text);
            
            // Call text-to-speech API with translated text
            const ttsResponse = await axios.post('http://localhost:5000/tts', {
                text: response.data.translated_text,
            });
            setAudioUrl(ttsResponse.data.audio_url);
        } catch (error) {
            console.error('Error translating text:', error);
        }
    };

    return (
        <div>
            <h1>Real-Time Translator</h1>
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to translate"
            />
            <input
                type="text"
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                placeholder="Enter target language"
            />
            <button onClick={handleTranslate}>Translate</button>
            <h2>Translated Text:</h2>
            <p>{translatedText}</p>
            {audioUrl && <audio controls src={audioUrl} />}
        </div>
    );
};

export default Translator;
