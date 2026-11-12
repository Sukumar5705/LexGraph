import React, { useState } from "react";

/**
 * SearchBar
 *
 * Allows the user to enter a legal research question
 * and sends it back to the parent component.
 */
export default function SearchBar({ onSearch, loading = false }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery || loading) {
      return;
    }

    onSearch(trimmedQuery);
  };

  return (
    <form className="searchbar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Ask a legal research question..."
        disabled={loading}
      />

      <button type="submit" disabled={loading || !query.trim()}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}