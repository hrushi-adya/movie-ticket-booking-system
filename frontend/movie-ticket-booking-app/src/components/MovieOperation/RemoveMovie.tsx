import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AddMovie: React.FC = () => {
  const navigate = useNavigate();
  const [responseMessage, setResponseMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [form, setForm] = useState({
    movie_name: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();


    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-Movie-DEV';

    try {
      const response = await fetch(`${apiGatewayUrl}?movie_name=${form.movie_name}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const result = await response.json();

      if (response.ok) {
        console.log('Delete Movie:', result);
        alert('Movie deleted successfully');
        navigate('/');
        setResponseMessage('Movie deleted successfully!');
      } else {
        setErrorMessage(result.message || 'Delete Operation failed. Please try again.');
      }
    } catch (error) {
      setErrorMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }

    alert(`Movie deleted: ${form.movie_name}`);
    setForm({
      movie_name: '',
    });
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <table>
        <tbody>
          <tr>
            <td>
              <label htmlFor="title">Enter Movie Name:</label>
            </td>
            <td>
              <input type="text" id="movie_name" name="movie_name" value={form.movie_name} onChange={handleChange} required />
            </td>
          </tr>
          <tr>
            <td colSpan={2}>
              <button type="submit" style={buttonStyle}>Submit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </form>
  );
};

const formStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '10px',
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#28a745',
  color: 'white',
  border: 'none',
  padding: '10px 15px',
  borderRadius: '5px',
  cursor: 'pointer',
};

export default AddMovie;
