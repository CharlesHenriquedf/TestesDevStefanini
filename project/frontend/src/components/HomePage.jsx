import React, { useState } from "react";
import api from "../api";

const HomePage = () => {
  const [activePage, setActivePage] = useState("register");
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
  });
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [responseMessage, setResponseMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleLoginChange = (e) => {
    const { name, value } = e.target;
    setLoginData({ ...loginData, [name]: value });
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/register", formData);
      setResponseMessage(`Sucesso: Usuário registrado com ID ${response.data.id}`);
    } catch (error) {
      setResponseMessage(`Erro: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/login", loginData);
      const token = response.data.access_token;
      localStorage.setItem("token", token);
      setResponseMessage("Login realizado com sucesso!");
      setLoginData({ email: "", password: "" }); 
    } catch (error) {
      setResponseMessage(`Erro no login: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleMovieSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get(`/search?query=${query}`);
      setMovies(response.data.results);
      setResponseMessage("Filmes encontrados:");
    } catch (error) {
      setResponseMessage(`Erro ao buscar filmes: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{ margin: "50px" }}>
      <h1>App de Testes</h1>
      <nav>
        <button onClick={() => setActivePage("register")}>Registrar</button>
        <button onClick={() => setActivePage("login")}>Login</button>
        <button onClick={() => setActivePage("movies")}>Buscar Filmes</button>
      </nav>

      {activePage === "register" && (
        <>
          <h2>Registro de Usuário</h2>
          <form onSubmit={handleRegisterSubmit}>
            <div>
              <label>Nome de Usuário:</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label>E-mail:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label>Senha:</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit">Registrar</button>
          </form>
        </>
      )}

      {activePage === "login" && (
        <>
          <h2>Login</h2>
          <form onSubmit={handleLoginSubmit}>
            <div>
              <label>E-mail:</label>
              <input
                type="email"
                name="email"
                value={loginData.email}
                onChange={handleLoginChange}
                required
              />
            </div>
            <div>
              <label>Senha:</label>
              <input
                type="password"
                name="password"
                value={loginData.password}
                onChange={handleLoginChange}
                required
              />
            </div>
            <button type="submit">Login</button>
          </form>
        </>
      )}

      {activePage === "movies" && (
        <>
          <h2>Buscar Filmes</h2>
          <form onSubmit={handleMovieSearch}>
            <div>
              <label>Filme:</label>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
              />
            </div>
            <button type="submit">Buscar</button>
          </form>
          <ul>
            {movies.map((movie) => (
              <li key={movie._id}>
                {movie.name} - Rotten Tomatoes: {movie.rottenTomatoesScore}%
              </li>
            ))}
          </ul>
        </>
      )}

      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
};

export default HomePage;
