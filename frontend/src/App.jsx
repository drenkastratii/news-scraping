import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NewsPage from "./components/News";
import AINewsPage from "./components/AI-News";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewsPage />} />
        <Route path="/ai-modified" element={<AINewsPage />} />
      </Routes>
    </Router>
  );
}

export default App;