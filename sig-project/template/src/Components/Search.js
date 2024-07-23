import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Search.css';

function SearchPage() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    if (query.trim()) {
      navigate(`/results?query=${query}`);
    }
  };

  return (
    <div className="searchContainer">
      <label htmlFor="game-name" className="search-label">게임 이름을 적어주세요</label><br />
      <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }}>
        <input
          type="text"
          id="game-name"
          name="gamename"
          placeholder="Value"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
}

export default SearchPage;