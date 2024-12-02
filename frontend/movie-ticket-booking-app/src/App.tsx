import './App.css';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';

import Home from './components/Home';
import Signup from './components/Signup';
import Signin from './components/Signin';
import { useAuth } from './components/AuthContext';
import Profile from './components/Profile';
import BookTicket from './components/BookTicket';
import MovieOperation from './components/MovieOperation/MovieOperation';

function App() {

  const { isLoggedIn, userType, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="App">
      <header className="App-header">
        <nav>
          <div className="nav-brand">UCM Movie Theatre</div>
          <div className="nav-links">
            <Link to="/">Home</Link>
            {isLoggedIn && userType === 'admin' && <Link to="/sales-dashboard">Sales Dashboard</Link>}
            {isLoggedIn && userType === 'admin' && <Link to="/movie-operation">Movie Operation</Link>}
            {!isLoggedIn && <Link to="/signin">Sign In</Link>}
            {!isLoggedIn && <Link to="/signup">Sign Up</Link>}
            {isLoggedIn && <button onClick={handleLogout}>Sign Out</button>}
            {isLoggedIn && <Link to="/profile">My Profile</Link>}
          </div>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/book" element={<BookTicket movie={{ title: '', description: '' }} />} />
          <Route path="/sales-dashboard" element={<div>Sales Dashboard</div>} />
          <Route path="/movie-operation" element={<MovieOperation />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
