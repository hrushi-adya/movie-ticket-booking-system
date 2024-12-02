import React, { useState } from 'react';

const AddMovie: React.FC = () => {
  const [form, setForm] = useState({ title: '', description: '', rating: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Movie added: ${form.title}`);
    setForm({ title: '', description: '', rating: '' });
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
    <h3>Add Movie</h3>
    <table>
      <tbody>
        <tr>
        <td>
          <label htmlFor="title">Title:</label>
        </td>
        <td>
          <input type="text" id="title" name="title" value={form.title} onChange={handleChange} required />
        </td>
        </tr>
        <tr>
        <td>
          <label htmlFor="description">Description:</label>
        </td>
        <td>
          <textarea id="description" name="description" value={form.description} onChange={handleChange} required />
        </td>
        </tr>
        <tr>
        <td>
          <label htmlFor="rating">Rating:</label>
        </td>
        <td>
          <input type="text" id="rating" name="rating" value={form.rating} onChange={handleChange} required />
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
