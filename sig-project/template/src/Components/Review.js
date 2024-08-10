import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Review.css';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBook, faVolumeUp, faDesktop, faLightbulb } from "@fortawesome/free-solid-svg-icons";

function ReviewPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('');

  const query = new URLSearchParams(location.search).get('query');

  useEffect(() => {
    if (query) {
      setSearchTerm(query);
      fetchData(query);
    }
  }, [query]);

  const fetchData = (term) => {
    setLoading(true);
    setError(null);
    setData(null);

    fetch(`http://localhost:8000/review?gamename=${encodeURIComponent(term)}`)
      .then(response => {
        if (!response.ok) {
          setLoading(false);
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          setData(data);
        } else {
        }
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        alert('오류');
        setLoading(false);
      });
  };

  const handleSearch = (event) => {
    event.preventDefault();
    if (searchTerm.trim()) {
      navigate(`?query=${encodeURIComponent(searchTerm.trim())}`);
    }
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  return (
    <div>
      <div className="header">
        <div className='projectName'>
          게임 리뷰 탐색기
        </div>
        <div className="keywords-container">
          <button className="keyword-button" onClick={() => handleCategoryChange('graphic')}><FontAwesomeIcon icon={faDesktop} />  그래픽</button>
          <button className="keyword-button" onClick={() => handleCategoryChange('sound')}><FontAwesomeIcon icon={faVolumeUp} />  사운드</button>
          <button className="keyword-button" onClick={() => handleCategoryChange('story')}><FontAwesomeIcon icon={faBook} />  스토리</button>
          <button className="keyword-button" onClick={() => handleCategoryChange('creativity')}><FontAwesomeIcon icon={faLightbulb} />  창의성</button>
        </div>

        <div className="search-container">
          <form id="searchForm" onSubmit={handleSearch}>
            <input
              type="text"
              name="gamename"
              id="gamename"
              placeholder="게임 이름"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <input type="submit" value="Search" />
          </form>
        </div>
      </div>

      <div className="main-content">
        <div className="game-name" id="gameName">
          {query}
        </div>

        <div className="evaluation-container">
          {selectedCategory === 'graphic' && (
            <>
              <div className="review">
                <div className='review-positiveheader'>긍정적리뷰<hr></hr></div>
                {data?.graphic || '그래픽 긍정 리뷰'}
              </div>
              <div className="review">
                <div className='review-negativeheader'>부정적리뷰<hr></hr></div>
                {data?.graphicNative || '그래픽 부정 리뷰'}
              </div>
            </>
          )}

          {selectedCategory === 'sound' && (
            <>
              <div className="review">
                <div className='review-positiveheader'>긍정적리뷰<hr></hr></div>
                {data?.sound || '사운드 긍정 리뷰'}
              </div>
              <div className="review">
                <div className='review-negativeheader'>부정적리뷰<hr></hr></div>
                {data?.soundNative || '사운드 부정 리뷰'}
              </div>
            </>
          )}

          {selectedCategory === 'story' && (
            <>
              <div className="review">
                <div className='review-positiveheader'>긍정적리뷰<hr></hr></div>
                {data?.story || '스토리 긍정 리뷰'}
              </div>
              <div className="review">
                <div className='review-negativeheader'>부정적리뷰<hr></hr></div>
                {data?.storyNative || '스토리 부정 리뷰'}
              </div>
            </>
          )}

          {selectedCategory === 'creativity' && (
            <>
              <div className="review">
                <div className='review-positiveheader'>긍정적리뷰<hr></hr></div>
                {data?.creativity || '창의성 긍정 리뷰'}
              </div>
              <div className="review">
                <div className='review-negativeheader'>부정적리뷰<hr></hr></div>
                {data?.creativityNative || '창의성 부정 리뷰'}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default ReviewPage;
