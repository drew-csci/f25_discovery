class PubMedSearchService:
    """
    A service to search for publications on PubMed (dummy implementation).
    """

    def search_publications(self, query: str, limit: int = 20) -> list[dict]:
        """
        Searches for publications based on a query and returns dummy results.

        Args:
            query (str): The search query.
            limit (int): The maximum number of results to return.

        Returns:
            list[dict]: A list of dictionaries, each representing a publication
                        with keys: 'title', 'journal', 'year', 'authors', 'link'.
        """
        # This is a dummy implementation. In a real application, this would
        # integrate with the PubMed API or a similar publication database.
        dummy_publications = [
            {
                'title': f"Dummy Publication 1 related to {query}",
                'journal': 'Journal of Dummy Science',
                'year': 2023,
                'authors': ['A. Author', 'B. Writer'],
                'link': 'https://pubmed.ncbi.nlm.nih.gov/dummy1/'
            },
            {
                'title': f"Another Dummy Study on {query} Research",
                'journal': 'Fictional Medical Journal',
                'year': 2022,
                'authors': ['C. Editor', 'D. Reviewer', 'E. Collaborator'],
                'link': 'https://pubmed.ncbi.nlm.nih.gov/dummy2/'
            },
            {
                'title': f"The Impact of {query} on Modern Society",
                'journal': 'Journal of Advanced Topics',
                'year': 2024,
                'authors': ['F. Pioneer'],
                'link': 'https://pubmed.ncbi.nlm.nih.gov/dummy3/'
            },
        ]
        return dummy_publications[:limit]
