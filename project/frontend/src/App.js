import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HistoryPage from "./components/HistoryPage";
import HomePage from "./components/HomePage";

const App = () => {
  return (
    <Router>
      <nav style={{ margin: "20px" }}>
        <Link to="/" style={{ margin: "10px" }}>
          Página Principal
        </Link>
        <Link to="/history" style={{ margin: "10px" }}>
          Histórico
        </Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </Router>
  );
};

export default App;
