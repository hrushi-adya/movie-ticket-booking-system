import React, { useState } from 'react';
import AddMovie from './AddMovie';
import EditMovie from './EditMovie';
import SearchMovie from './SearchMovie';
import RemoveMovie from './RemoveMovie';

const MovieOperation: React.FC = () => {
  const [activeOperation, setActiveOperation] = useState<string | null>(null);

  const handleOperationClick = (operation: string) => {
    setActiveOperation(operation);
  };

  return (
    <div style={containerStyle}>
      <h2>Movie Operations</h2>
      <div style={buttonContainerStyle}>
        <button onClick={() => handleOperationClick('add')} style={buttonStyle}>
          Add Movie
        </button>
        <button onClick={() => handleOperationClick('edit')} style={buttonStyle}>
          Edit Movie
        </button>
        <button onClick={() => handleOperationClick('search')} style={buttonStyle}>
          Search Movie
        </button>
        <button onClick={() => handleOperationClick('remove')} style={buttonStyle}>
          Remove Movie
        </button>
      </div>

      <div style={operationContainerStyle}>
        {activeOperation === 'add' && <AddMovie />}
        {activeOperation === 'edit' && <EditMovie />}
        {activeOperation === 'search' && <SearchMovie />}
        {activeOperation === 'remove' && <RemoveMovie />}
      </div>
    </div>
  );
};

const containerStyle: React.CSSProperties = {
  padding: '20px',
  maxWidth: '800px',
  margin: '0 auto',
};

const buttonContainerStyle: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  marginBottom: '20px',
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#007bff',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  borderRadius: '5px',
  cursor: 'pointer',
  fontSize: '16px',
};

const operationContainerStyle: React.CSSProperties = {
  marginTop: '20px',
};

export default MovieOperation;
