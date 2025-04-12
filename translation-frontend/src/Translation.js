import React, { useState } from 'react';
import axios from 'axios';

const Translation = () => {
  const [text, setText] = useState('');
  const [targetLang, setTargetLang] = useState('es');
  const [translatedText, setTranslatedText] = useState('');
  const [error, setError] = useState('');

  const handleTranslate = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/translate', {
        text,
        target_lang: targetLang,
      });
      setTranslatedText(response.data.translated_text);
      setError('');
    } catch (err) {
      setError('Translation failed. Please try again.');
    }
  };

  return (
    <div>
      <h1>Text Translation App</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to translate"
      />
      <div>
        <label>Target Language: </label>
        <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="it">Italian</option>
          <option value="ja">Japanese</option>
          {/* Add more languages as needed */}
        </select>
      </div>
      <button onClick={handleTranslate}>Translate</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {translatedText && <p>Translated Text: {translatedText}</p>}
    </div>
  );
};

export default Translation;
