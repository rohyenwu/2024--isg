import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Review.css';

function ReviewPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const query = new URLSearchParams(location.search).get('query');

  // URL 쿼리 파라미터가 변경되면 해당 쿼리로 데이터를 fetch합니다
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
        if(data)
          setData(data);
        else
          alert('게임이 존재하지 않습니다.');
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
      // URL 쿼리 파라미터 업데이트
      navigate(`?query=${encodeURIComponent(searchTerm.trim())}`);
    }
  };

  // 로딩 중일 때
  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
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
        <div className="game-name" id="gameName">
          {query || '게임 이름을 입력하세요'}
        </div>
      </div>
      <div className="evaluation-container">
        <div>
          <label>그래픽</label>
          <div className="review" id="graphicReview">{data?.graphic || '그래픽 긍정 리뷰'}</div>
        </div>
        <div>
          <label>사운드</label>
          <div className="review" id="soundReview">{data?.sound || '사운드 긍정 리뷰'}</div>
        </div>
        <div>
          <label>스토리</label>
          <div className="review" id="storyReview">{data?.story || '스토리 긍정 리뷰'}</div>
        </div>
        <div>
          <label>창의성</label>
          <div className="review" id="creativityReview">{data?.creativity || '창의성 긍정 리뷰'}</div>
        </div>
        <div className="new-row"></div>
        <div>
          <div className="review" id="graphicNativeReview">{data?.graphicNative || '그래픽 부정 리뷰'}</div>
          <div className="score" id="graphicScore">{data?.graphicScore}</div>
        </div>
        <div>
          <div className="review" id="soundNativeReview">{data?.soundNative || '사운드 부정 리뷰'}</div>
          <div className="score" id="soundScore">{data?.soundScore}</div>
        </div>
        <div>
          <div className="review" id="storyNativeReview">{data?.storyNative || '스토리 부정 리뷰'}</div>
          <div className="score" id="storyScore">{data?.storyScore}</div>
        </div>
        <div>
          <div className="review" id="creativityNativeReview">{data?.creativityNative || '창의성 부정 리뷰'}</div>
          <div className="score" id="creativityScore">{data?.creativityScore}</div>
        </div>
      </div>
    </div>
  );
}

export default ReviewPage;
