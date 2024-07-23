import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './Components/Search';
import ReviewPage from './Components/Review';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/results" element={<ReviewPage />} />
      </Routes>
    </Router>
  );
}

export default App;