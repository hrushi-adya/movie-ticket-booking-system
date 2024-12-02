import React from 'react';

const RemoveMovie: React.FC = () => {
  const handleRemoveAll = () => {
    if (window.confirm('Are you sure you want to remove all movies?')) {
      alert('All movies removed!');
    }
  };

  return (
    <div>
      <h3>Remove Movie</h3>
      <button onClick={handleRemoveAll} style={buttonStyle}>Remove All Movies</button>
    </div>
  );
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#dc3545',
  color: 'white',
  border: 'none',
  padding: '10px 15px',
  borderRadius: '5px',
  cursor: 'pointer',
};

export default RemoveMovie;
