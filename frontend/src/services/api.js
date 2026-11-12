/**
 * API client for the Authority- and Temporal-Aware GraphRAG backend.
 */

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";


// =========================================================
// SEARCH
// =========================================================

export async function searchQuery(
  query,
  top_k = 10,
  retrieval_k = 20,
  reference_date = "2024-01-01"
) {
  const response = await fetch(`${API_BASE_URL}/api/search/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k,
      retrieval_k,
      reference_date,
    }),
  });

  if (!response.ok) {
    let errorMessage = `Search request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}


// =========================================================
// GET CASE
// =========================================================

export async function getCase(caseId) {
  const response = await fetch(
    `${API_BASE_URL}/api/cases/${encodeURIComponent(caseId)}`
  );

  if (!response.ok) {
    let errorMessage = `Case request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}


// =========================================================
// GET GRAPH SUBGRAPH
// =========================================================

export async function getSubgraph(caseId) {
  const response = await fetch(
    `${API_BASE_URL}/api/graph/subgraph?case_id=${encodeURIComponent(caseId)}`
  );

  if (!response.ok) {
    let errorMessage = `Graph request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}


// =========================================================
// EXPORT
// =========================================================

export { API_BASE_URL };