import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import KnowledgeGraph from "../components/KnowledgeGraph";
import { searchQuery } from "../services/api";

/**
 * Home page
 *
 * Main legal research interface.
 * Sends the question to the FastAPI GraphRAG backend
 * and presents the answer, retrieved cases, knowledge graph,
 * citation verification, and conflict detection.
 */
export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (query) => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      console.log("[FRONTEND] Sending search request:", query);

      const data = await searchQuery(
        query,
        10,
        20,
        "2024-01-01"
      );

      console.log("[FRONTEND] Search response:", data);

      setResult(data);
    } catch (err) {
      console.error("[FRONTEND] Search error:", err);

      setError(
        err.message ||
          "Something went wrong while searching."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     CITATION VERIFICATION DATA
     ======================================================= */

  const verification =
    result?.citation_verification || {};

  const conflict =
    result?.conflict_report || {};

  const verifiedCases =
    verification.verified_case_ids || [];

  const unverifiedCases =
    verification.unverified_case_ids || [];

  const verifiedScc =
    verification.verified_scc_citations || [];

  const unverifiedScc =
    verification.unverified_scc_citations || [];

  const totalVerified =
    verifiedCases.length +
    verifiedScc.length;

  const totalUnverified =
    unverifiedCases.length +
    unverifiedScc.length;


  /* =======================================================
     KNOWLEDGE GRAPH CASE

     Prefer the first retrieved source because that is the
     primary case displayed to the user in Retrieved Cases.

     Fall back to relevant_sources only if sources is empty.
     ======================================================= */

  const graphCaseId =
    result?.sources?.[0]?.case_id ||
    result?.relevant_sources?.[0]?.case_id ||
    null;


  return (
    <main className="home-page">

      {/* ===================================================
          HERO
          =================================================== */}

      <section className="hero-section">

        <h1>
          Authority- and Temporal-Aware
          <br />
          Legal GraphRAG
        </h1>

        <p>
          Search Indian legal precedents using
          authority-aware and evidence-grounded
          retrieval.
        </p>

      </section>


      {/* ===================================================
          SEARCH
          =================================================== */}

      <section className="search-section">

        <SearchBar
          onSearch={handleSearch}
          loading={loading}
        />

      </section>


      {/* ===================================================
          LOADING
          =================================================== */}

      {loading && (
        <section className="status-message">

          <p>
            Searching legal precedents, analyzing
            authority, and generating an
            evidence-grounded answer...
          </p>

        </section>
      )}


      {/* ===================================================
          ERROR
          =================================================== */}

      {error && (
        <section className="error-message">

          <h3>
            Search Error
          </h3>

          <p>
            {error}
          </p>

        </section>
      )}


      {/* ===================================================
          SEARCH RESULTS
          =================================================== */}

      {result && !loading && (

        <section className="search-result">


          {/* =================================================
              GENERATED LEGAL ANSWER
              ================================================= */}

          <div className="answer-section">

            <div className="section-header">

              <div>

                <span className="section-label">
                  LEGAL RESEARCH RESULT
                </span>

                <h2>
                  Generated Legal Answer
                </h2>

              </div>

            </div>


            <div className="answer-content">

              {result.answer ||
                "No answer returned."}

            </div>

          </div>


          {/* =================================================
              RETRIEVED CASES
              ================================================= */}

          {result.sources &&
            result.sources.length > 0 && (

              <div className="sources-section">

                <div className="section-header">

                  <div>

                    <span className="section-label">
                      RETRIEVED EVIDENCE
                    </span>

                    <h2>
                      Retrieved Cases
                    </h2>

                  </div>


                  <span className="result-count">
                    {result.sources.length} sources
                  </span>

                </div>


                <div className="source-list">

                  {result.sources.map(
                    (source, index) => {

                      const caseId =
                        source.case_id ||
                        `Source ${index + 1}`;

                      const title =
                        source.title ||
                        "Indian legal precedent";


                      return (

                        <div
                          className="source-card"
                          key={index}
                        >

                          <div className="source-number">
                            {String(index + 1).padStart(
                              2,
                              "0"
                            )}
                          </div>


                          <div className="source-main">

                            <h3>
                              {caseId}
                            </h3>


                            <p className="case-title">
                              {title}
                            </p>


                            <div className="source-meta">

                              {source.court && (
                                <span>
                                  <strong>
                                    Court:
                                  </strong>{" "}
                                  {source.court}
                                </span>
                              )}


                              {source.decision_date && (
                                <span>
                                  <strong>
                                    Date:
                                  </strong>{" "}
                                  {source.decision_date}
                                </span>
                              )}

                            </div>

                          </div>

                        </div>

                      );
                    }
                  )}

                </div>

              </div>

            )}


          {/* =================================================
              KNOWLEDGE GRAPH
              ================================================= */}

          {graphCaseId && (
            <KnowledgeGraph
              caseId={graphCaseId}
            />
          )}


          {/* =================================================
              CITATION VERIFICATION
              ================================================= */}

          {result.citation_verification && (

            <div className="verification-section">

              <div className="section-header">

                <div>

                  <span className="section-label">
                    EVIDENCE CHECK
                  </span>

                  <h2>
                    Citation Verification
                  </h2>

                </div>


                <div
                  className={
                    verification.verified
                      ? "verification-badge verified"
                      : "verification-badge warning"
                  }
                >
                  {verification.verified
                    ? "Verified"
                    : "Review Required"}
                </div>

              </div>


              {/* ---------------------------------------------
                  Verification summary
                  --------------------------------------------- */}

              <div className="verification-summary">

                <div className="verification-stat">

                  <span className="stat-number">
                    {totalVerified}
                  </span>

                  <span className="stat-label">
                    Verified
                  </span>

                </div>


                <div className="verification-stat">

                  <span className="stat-number warning-number">
                    {totalUnverified}
                  </span>

                  <span className="stat-label">
                    Needs Verification
                  </span>

                </div>

              </div>


              {/* ---------------------------------------------
                  Verified case citations
                  --------------------------------------------- */}

              {verifiedCases.length > 0 && (

                <div className="citation-group">

                  <h3>
                    ✓ Verified Case Citations
                  </h3>


                  {verifiedCases.map(
                    (citation, index) => (

                      <div
                        className="citation-item verified-item"
                        key={index}
                      >
                        {citation}
                      </div>

                    )
                  )}

                </div>

              )}


              {/* ---------------------------------------------
                  Unverified case citations
                  --------------------------------------------- */}

              {unverifiedCases.length > 0 && (

                <div className="citation-group">

                  <h3>
                    ⚠ Unverified Case Citations
                  </h3>


                  {unverifiedCases.map(
                    (citation, index) => (

                      <div
                        className="citation-item warning-item"
                        key={index}
                      >
                        {citation}
                      </div>

                    )
                  )}

                </div>

              )}


              {/* ---------------------------------------------
                  Verified SCC citations
                  --------------------------------------------- */}

              {verifiedScc.length > 0 && (

                <div className="citation-group">

                  <h3>
                    ✓ Verified SCC Citations
                  </h3>


                  {verifiedScc.map(
                    (citation, index) => (

                      <div
                        className="citation-item verified-item"
                        key={index}
                      >
                        {citation}
                      </div>

                    )
                  )}

                </div>

              )}


              {/* ---------------------------------------------
                  Unverified SCC citations
                  --------------------------------------------- */}

              {unverifiedScc.length > 0 && (

                <div className="citation-group">

                  <h3>
                    ⚠ SCC Citations Requiring Verification
                  </h3>


                  {unverifiedScc.map(
                    (citation, index) => (

                      <div
                        className="citation-item warning-item"
                        key={index}
                      >
                        {citation}
                      </div>

                    )
                  )}

                </div>

              )}


              {/* ---------------------------------------------
                  Verification explanation
                  --------------------------------------------- */}

              {verification.verification_reason && (

                <p className="verification-note">
                  {verification.verification_reason}
                </p>

              )}

            </div>

          )}


          {/* =================================================
              CONFLICT DETECTION
              ================================================= */}

          {result.conflict_report && (

            <div className="conflict-section">

              <div className="section-header">

                <div>

                  <span className="section-label">
                    LEGAL CONSISTENCY CHECK
                  </span>

                  <h2>
                    Conflict Detection
                  </h2>

                </div>


                <div
                  className={
                    conflict.conflict_detected
                      ? "verification-badge warning"
                      : "verification-badge verified"
                  }
                >

                  {conflict.conflict_detected
                    ? "Conflict Detected"
                    : "No Conflict Detected"}

                </div>

              </div>


              <div className="conflict-summary">

                <div className="conflict-icon">

                  {conflict.conflict_detected
                    ? "⚠"
                    : "✓"}

                </div>


                <div>

                  <h3>

                    {conflict.conflict_detected
                      ? "Potential legal conflicts found"
                      : "Retrieved evidence is consistent"}

                  </h3>


                  <p>

                    {conflict.conflict_count || 0}{" "}
                    conflict(s) detected among the
                    retrieved evidence.

                  </p>

                </div>

              </div>


              {/* ---------------------------------------------
                  Conflict details
                  --------------------------------------------- */}

              {conflict.conflicts &&
                conflict.conflicts.length > 0 && (

                  <div className="conflict-list">

                    {conflict.conflicts.map(
                      (item, index) => (

                        <div
                          className="conflict-item"
                          key={index}
                        >

                          {typeof item === "string"
                            ? item
                            : JSON.stringify(item)}

                        </div>

                      )
                    )}

                  </div>

                )}

            </div>

          )}

        </section>

      )}

    </main>
  );
}