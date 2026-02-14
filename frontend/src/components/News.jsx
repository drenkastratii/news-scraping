import React, { useState, useEffect } from "react";

function NewsPage() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await fetch("http://localhost:8000/news/");
        if (!response.ok) throw new Error("error");

        const data = await response.json();
        setNews(data);
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  const filteredNews = news.filter((item) => {
    if (!query) return true;
    const q = query.toLowerCase();
    return (
      item.news_title?.toLowerCase().includes(q) ||
      item.news_text?.toLowerCase().includes(q) ||
      item.news_portal?.toLowerCase().includes(q)
    );
  });

  const hasArticles = filteredNews.length > 0;
  const [featured, ...rest] = hasArticles ? filteredNews : [null, []];

  return (
    <div className="page-root">
      <header className="site-header">
        <div className="site-header-inner">
          <div className="brand">
            <img
              src="/news-logo.png"
              alt="News app logo"
              className="brand-logo"
            />
            <div className="brand-copy">
              <span className="brand-name">LiveWire News</span>
              <span className="brand-tagline">
                Your real-time news briefing
              </span>
            </div>
          </div>

          <nav className="primary-nav" aria-label="Primary">
            <button className="nav-pill nav-pill--primary" type="button">
              Top stories
            </button>
            <button className="nav-pill" type="button">
              World
            </button>
            <button className="nav-pill" type="button">
              Tech
            </button>
            <button className="nav-pill" type="button">
              Business
            </button>
            <button className="nav-pill" type="button">
              Sports
            </button>
          </nav>

          <div className="header-spacer" />

          <div className="header-actions">
            <input
              type="search"
              className="search-input"
              placeholder="Search headlines…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              aria-label="Search news"
            />
            <span className="user-pill">Live feed</span>
          </div>
        </div>
      </header>

      <main className="page-main">
        {loading ? (
          <div className="loading-state">
            <div className="spinner" />
            <p>Fetching the latest headlines…</p>
          </div>
        ) : !hasArticles ? (
          <div className="empty-state">
            <div className="empty-title">No headlines just yet</div>
            <div className="empty-caption">
              Try clearing your search or check back in a moment for fresh
              updates.
            </div>
          </div>
        ) : (
          <>
            <section className="hero-and-sidebar" aria-label="Featured story">
              <article className="hero-card">
                <div className="hero-orbit" aria-hidden="true" />
                <div className="hero-card-inner">
                  <div className="hero-pill-row">
                    <span className="hero-label">Top story</span>
                    <span className="hero-live">
                      <span className="hero-badge-dot" />
                      Live
                    </span>
                    <span className="hero-meta">
                      {featured?.news_portal || "LiveWire desk"}
                    </span>
                  </div>

                  <h1 className="hero-title">{featured?.news_title}</h1>
                  <p className="hero-body">{featured?.news_text}</p>

                  <div className="hero-footer">
                    <p className="hero-source">
                      Curated from{" "}
                      <strong>
                        {featured?.news_portal || "multiple verified sources"}
                      </strong>
                    </p>
                    <button type="button" className="hero-cta">
                      View full coverage
                    </button>
                  </div>
                </div>
              </article>

              <aside className="sidebar-card" aria-label="Trending now">
                <div className="sidebar-header">
                  <h2 className="sidebar-title">Trending now</h2>
                  <span className="sidebar-subtitle">
                    {Math.min(rest.length, 5)} headlines
                  </span>
                </div>
                <ul className="sidebar-list">
                  {rest.slice(0, 5).map((item) => (
                    <li key={item.id} className="sidebar-item">
                      <div className="sidebar-item-title">
                        {item.news_title}
                      </div>
                      <div className="sidebar-item-meta">
                        {item.news_portal || "Source"}
                      </div>
                    </li>
                  ))}
                </ul>
              </aside>
            </section>

            <section
              className="news-grid-section"
              aria-label="Latest updates"
            >
              <div className="section-heading-row">
                <h2 className="section-title">Latest updates</h2>
                <p className="section-caption">
                  A concise, real-time digest of what&apos;s happening now.
                </p>
              </div>

              <div className="news-grid">
                {rest.map((item) => (
                  <article key={item.id} className="news-card">
                    <div className="news-card-inner">
                      <div className="news-card-tag">
                        <span>{item.news_portal || "LiveWire"}</span>
                      </div>
                      <h3 className="news-card-title">{item.news_title}</h3>
                      <p className="news-card-body">{item.news_text}</p>
                      <div className="news-card-footer">
                        <span>Just now</span>
                        <a
                          href="#"
                          className="news-card-link"
                          onClick={(e) => e.preventDefault()}
                        >
                          Read brief
                        </a>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          </>
        )}
      </main>

      <footer className="site-footer">
        <span>LiveWire News</span> · Curating real-time headlines from your
        favorite portals.
      </footer>
    </div>
  );
}

export default NewsPage;