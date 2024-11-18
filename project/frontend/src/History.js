import React, { useState } from "react";
import api from "./api";

const History = () => {
  const [history, setHistory] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [historyMessage, setHistoryMessage] = useState("");

  const fetchHistory = async () => {
    try {
      const response = await api.get("/history"); // Rota de histórico
      setHistory(response.data.history);
      setPagination(response.data.pagination);
      setHistoryMessage("Histórico carregado:");
    } catch (error) {
      setHistoryMessage(`Erro ao carregar histórico: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div style={{ margin: "50px" }}>
      <h1>Histórico de Buscas</h1>
      <button onClick={fetchHistory}>Carregar Histórico</button>
      <p>{historyMessage}</p>
      <ul>
        {history.map((entry) => (
          <li key={entry._id}>
            {entry.movie_title} - Data: {new Date(entry.search_date).toLocaleString()}
          </li>
        ))}
      </ul>
      {pagination && (
        <p>
          Página: {pagination.page} de {pagination.total_pages} | Total: {pagination.total_count}
        </p>
      )}
    </div>
  );
};

export default History;
