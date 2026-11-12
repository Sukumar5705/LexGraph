import React, { useEffect, useState } from "react";
import { getSubgraph } from "../services/api";

/**
 * KnowledgeGraph
 *
 * Displays the citation subgraph returned by the backend.
 *
 * This component uses the real knowledge graph API.
 * It does not create mock or hardcoded graph data.
 */
export default function KnowledgeGraph({ caseId }) {
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!caseId) {
      setGraph(null);
      return;
    }

    const loadGraph = async () => {
      setLoading(true);
      setError("");

      try {
        console.log(
          "[GRAPH] Loading subgraph for:",
          caseId
        );

        const data = await getSubgraph(caseId);

        console.log(
          "[GRAPH] Subgraph response:",
          data
        );

        setGraph(data);
      } catch (err) {
        console.error(
          "[GRAPH] Failed to load graph:",
          err
        );

        setError(
          err.message ||
          "Unable to load knowledge graph."
        );
      } finally {
        setLoading(false);
      }
    };

    loadGraph();
  }, [caseId]);

  if (!caseId) {
    return null;
  }

  return (
    <section className="knowledgegraph-section">

      {/* =================================================
          HEADER
          ================================================= */}

      <div className="section-header">

        <div>
          <span className="section-label">
            KNOWLEDGE GRAPH
          </span>

          <h2>Case Citation Network</h2>
        </div>

        {graph && (
          <div className="graph-count">
            {graph.node_count || 0} nodes ·{" "}
            {graph.edge_count || 0} relationships
          </div>
        )}

      </div>


      {/* =================================================
          LOADING
          ================================================= */}

      {loading && (
        <div className="graph-status">
          Loading citation relationships...
        </div>
      )}


      {/* =================================================
          ERROR
          ================================================= */}

      {error && (
        <div className="graph-error">
          {error}
        </div>
      )}


      {/* =================================================
          GRAPH
          ================================================= */}

      {!loading && !error && graph && (

        <div className="graph-container">

          {/* ---------------------------------------------
              Graph explanation
              --------------------------------------------- */}

          <div className="graph-description">

            <p>
              This graph shows citation relationships
              available in the legal knowledge graph for
              the selected case.
            </p>

          </div>


          {/* ---------------------------------------------
              Nodes
              --------------------------------------------- */}

          <div className="graph-nodes">

            {graph.nodes &&
              graph.nodes.map((node) => (

                <div
                  className={
                    node.role === "selected_case"
                      ? "graph-node selected"
                      : "graph-node"
                  }
                  key={node.id}
                >

                  <div className="graph-node-type">
                    {node.role === "selected_case"
                      ? "SELECTED CASE"
                      : node.role === "cited_case"
                        ? "CITED CASE"
                        : "CITING CASE"}
                  </div>

                  <div className="graph-node-case">
                    {node.case_id || "Unknown case"}
                  </div>

                  {node.title && (
                    <div className="graph-node-title">
                      {node.title}
                    </div>
                  )}

                  {node.citation && (
                    <div className="graph-node-citation">
                      {node.citation}
                    </div>
                  )}

                  {node.decision_date && (
                    <div className="graph-node-date">
                      Decision date:{" "}
                      {node.decision_date}
                    </div>
                  )}

                </div>

              ))}

          </div>


          {/* ---------------------------------------------
              Relationships
              --------------------------------------------- */}

          {graph.edges &&
            graph.edges.length > 0 && (

              <div className="graph-relationships">

                <h3>
                  Citation Relationships
                </h3>

                {graph.edges.map(
                  (edge, index) => (

                    <div
                      className="graph-edge"
                      key={index}
                    >

                      <span>
                        {graph.nodes.find(
                          (node) =>
                            node.id === edge.source
                        )?.case_id ||
                          edge.source}
                      </span>

                      <strong>
                        →
                      </strong>

                      <span>
                        {graph.nodes.find(
                          (node) =>
                            node.id === edge.target
                        )?.case_id ||
                          edge.target}
                      </span>

                      <small>
                        {edge.relationship}
                      </small>

                    </div>

                  )
                )}

              </div>
            )}


          {/* ---------------------------------------------
              No relationships
              --------------------------------------------- */}

          {graph.edges &&
            graph.edges.length === 0 && (

              <div className="graph-empty">

                <div className="graph-empty-icon">
                  ○
                </div>

                <div>

                  <h3>
                    No citation relationships found
                  </h3>

                  <p>
                    The selected case exists in the
                    knowledge graph, but no connected
                    citation relationship was found for
                    this one-hop subgraph.
                  </p>

                </div>

              </div>
            )}

        </div>
      )}

    </section>
  );
}