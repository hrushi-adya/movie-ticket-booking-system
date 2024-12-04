import './App.css';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';

import Home from './components/Home';
import Signup from './components/Signup';
import Signin from './components/Signin';
import { useAuth } from './components/AuthContext';
import Profile from './components/Profile';
import BookTicket from './components/BookTicket';
import MovieOperation from './components/MovieOperation/MovieOperation';
import MyShows from './components/MyShows';
import SalesDashboard from './components/SalesDashboard';

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
            {isLoggedIn && <Link to="/movie-history">My Shows</Link>}
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
          <Route path="/sales-dashboard" element={<SalesDashboard />} />
          <Route path="/movie-operation" element={<MovieOperation />} />
          <Route path="/movie-history" element={<MyShows />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
