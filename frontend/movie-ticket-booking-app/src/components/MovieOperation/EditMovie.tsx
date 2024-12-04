import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AddMovie: React.FC = () => {
  const navigate = useNavigate();
  const [responseMessage, setResponseMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [form, setForm] = useState({
    movie_name: '',
    movie_description: '',
    genre: '',
    movie_director: '',
    release_date: '',
    ticket_price: '',
    movie_length: '',
    movie_thumbnail: '',
    movie_available: '',
    movie_showtimes: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      // movie_name: form.movie_name,
      movie_description: form.movie_description,
      genre: form.genre,
      movie_director: form.movie_director,
      release_date: form.release_date,
      ticket_price: form.ticket_price,
      movie_length: form.movie_length,
      movie_thumbnail: form.movie_thumbnail,
      movie_available: form.movie_available,
      movie_showtimes: form.movie_showtimes,
    };
    console.log('Movie Data:', payload);
    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-Movie-DEV';

    try {
      const response = await fetch(`${apiGatewayUrl}?movie_name=${form.movie_name}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok) {
        console.log('Edit Movie Result:', result);
        alert('Movie updated successfully');
        navigate('/');
        setResponseMessage('Movie Added successfully!');
      } else {
        setErrorMessage(result.message || 'Edit Operation failed. Please try again.');
      }
    } catch (error) {
      setErrorMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }

    alert(`Movie updated: ${form.movie_name}`);
    setForm({
      movie_name: '',
      movie_description: '',
      genre: '',
      movie_director: '',
      release_date: '',
      ticket_price: '',
      movie_length: '',
      movie_thumbnail: '',
      movie_available: '',
      movie_showtimes: ''
    });
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h3>Update Movie Details</h3>
      <table>
        <tbody>
          <tr>
            <td>
              <label htmlFor="title">Title:</label>
            </td>
            <td>
              <input type="text" id="movie_name" name="movie_name" value={form.movie_name} onChange={handleChange} required />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_description">Description:</label>
            </td>
            <td>
              <textarea id="movie_description" name="movie_description" value={form.movie_description} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="genre">Genre:</label>
            </td>
            <td>
              <input type="text" id="genre" name="genre" value={form.genre} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_director">Director:</label>
            </td>
            <td>
              <input type="text" id="movie_director" name="movie_director" value={form.movie_director} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="release_date">Release Date:</label>
            </td>
            <td>
              <input type="date" id="release_date" name="release_date" value={form.release_date} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="ticket_price">Ticket Price:</label>
            </td>
            <td>
              <input type="number" id="ticket_price" name="ticket_price" value={form.ticket_price} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_length">Length:</label>
            </td>
            <td>
              <input type="text" id="movie_length" name="movie_length" value={form.movie_length} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_thumbnail">Thumbnail URL:</label>
            </td>
            <td>
              <input type="text" id="movie_thumbnail" name="movie_thumbnail" value={form.movie_thumbnail} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_available">Available:</label>
            </td>
            <td>
              <input type="text" id="movie_available" name="movie_available" value={form.movie_available} onChange={handleChange} />
            </td>
          </tr>
          <tr>
            <td>
              <label htmlFor="movie_showtimes">Showtimes:</label>
            </td>
            <td>
              <input type="text" id="movie_showtimes" name="movie_showtimes" value={form.movie_showtimes} onChange={handleChange} />
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
