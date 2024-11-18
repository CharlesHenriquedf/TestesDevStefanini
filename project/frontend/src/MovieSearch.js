import React, { useState } from "react";
import api from "./api";

const MovieSearch = () => {
  const [query, setQuery] = useState("");
  const [movies, setMovies] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");

  const handleMovieSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get(`/search?query=${query}`); // Rota de busca de filmes
      setMovies(response.data.results);
      setSearchMessage("Filmes encontrados:");
    } catch (error) {
      setSearchMessage(`Erro ao buscar filmes: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{ margin: "50px" }}>
      <h1>Buscar Filmes</h1>
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
      <p>{searchMessage}</p>
      <ul>
        {movies.map((movie) => (
          <li key={movie._id}>
            {movie.name} - Rotten Tomatoes: {movie.rottenTomatoesScore}%
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MovieSearch;
