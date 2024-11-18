import React, { useEffect, useState } from "react";
import api from "../api";
import "./HistoryPage.css"; // Arquivo de estilos para tabela

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get("/history");
        setHistory(response.data.history);
      } catch (error) {
        setErrorMessage(`Erro ao carregar histórico: ${error.response?.data?.detail || error.message}`);
      }
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>Histórico de Buscas</h2>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      <table className="history-table">
        <thead>
          <tr>
            <th>Título do Filme</th>
            <th>Data da Busca</th>
          </tr>
        </thead>
        <tbody>
          {history.map((entry) => (
            <tr key={entry._id}>
              <td>{entry.movie_title}</td>
              <td>{new Date(entry.search_date).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryPage;
