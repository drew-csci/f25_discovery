from django.test import TestCase
from pages.services import PubMedSearchService

class PubMedSearchServiceTests(TestCase):
    def test_search_publications_structure_and_length(self):
        """
        Test that search_publications returns a list of dictionaries with the
        expected structure and length.
        """
        service = PubMedSearchService()
        query = "gene therapy"
        publications = service.search_publications(query)

        self.assertIsInstance(publications, list)
        self.assertGreater(len(publications), 0)
        self.assertLessEqual(len(publications), 20)  # Default limit is 20

        for publication in publications:
            self.assertIsInstance(publication, dict)
            self.assertIn('title', publication)
            self.assertIn('journal', publication)
            self.assertIn('year', publication)
            self.assertIn('authors', publication)
            self.assertIn('link', publication)

            self.assertIsInstance(publication['title'], str)
            self.assertIsInstance(publication['journal'], str)
            self.assertIsInstance(publication['year'], int)
            self.assertIsInstance(publication['authors'], list)
            self.assertIsInstance(publication['link'], str)

            for author in publication['authors']:
                self.assertIsInstance(author, str)

            self.assertIn(query.lower(), publication['title'].lower() or publication['journal'].lower())
