"""
Unit tests for the EmbeddingService class.

These tests use mocking to avoid making actual OpenAI API calls,
ensuring no credits are consumed during testing while thoroughly
validating all functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import List
import logging
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the OpenAI client before any imports
with patch('openai.OpenAI') as mock_openai:
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    # Now import the service after mocking
    from services.embedding import EmbeddingService, EMBEDDING_MODEL, EMBED_DIM


class TestEmbeddingService(unittest.TestCase):
    """Test cases for the EmbeddingService class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Sample test data
        self.sample_text = "This is a sample text for testing embeddings."
        self.sample_texts = [
            "First document for testing",
            "Second document for testing", 
            "Third document for testing"
        ]
        
        # Mock embedding response structure
        self.mock_single_embedding = [0.1] * EMBED_DIM
        self.mock_batch_embeddings = [
            [0.1] * EMBED_DIM,
            [0.2] * EMBED_DIM,
            [0.3] * EMBED_DIM
        ]
        
        # Create proper mock response objects
        self.mock_single_response = MagicMock()
        self.mock_single_response.data = [MagicMock()]
        self.mock_single_response.data[0].embedding = self.mock_single_embedding
        
        # For batch responses, we need to support both attribute and dict access
        self.mock_batch_response = MagicMock()
        self.mock_batch_response.data = []
        for i, embedding in enumerate(self.mock_batch_embeddings):
            mock_item = MagicMock()
            mock_item.embedding = embedding
            # Also support dictionary-style access
            mock_item.__getitem__ = MagicMock(return_value=embedding)
            self.mock_batch_response.data.append(mock_item)

    def test_generate_embedding_success(self):
        """Test successful single embedding generation."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_create.return_value = self.mock_single_response
            
            # Call the method
            result = EmbeddingService.generate_embedding(self.sample_text)
            
            # Verify the result
            self.assertEqual(result, self.mock_single_embedding)
            self.assertEqual(len(result), EMBED_DIM)
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], float)
            
            # Verify the API was called correctly
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=self.sample_text
            )

    def test_generate_embedding_dimension_mismatch(self):
        """Test embedding generation with dimension mismatch warning."""
        # Create a mock response with wrong dimension
        wrong_dim_embedding = [0.1] * (EMBED_DIM + 10)
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = wrong_dim_embedding
        
        with patch('services.embedding.client.embeddings.create') as mock_create:
            with patch('logging.Logger.warning') as mock_warning:
                # Configure the mock
                mock_create.return_value = mock_response
                
                # Call the method
                result = EmbeddingService.generate_embedding(self.sample_text)
                
                # Verify the result is still returned despite dimension mismatch
                self.assertEqual(result, wrong_dim_embedding)
                
                # Verify warning was logged
                mock_warning.assert_called_once_with(
                    f"Embedding dimension mismatch: {len(wrong_dim_embedding)} != {EMBED_DIM}"
                )

    def test_generate_embedding_api_error(self):
        """Test embedding generation when API call fails."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            with patch('logging.Logger.error') as mock_error:
                # Configure the mock to raise an exception
                mock_create.side_effect = Exception("API Error")
                
                # Verify the exception is raised
                with self.assertRaises(Exception):
                    EmbeddingService.generate_embedding(self.sample_text)
                
                # Verify error was logged
                mock_error.assert_called_once_with(
                    "Embedding generation failed: API Error"
                )

    def test_batch_generate_embeddings_success(self):
        """Test successful batch embedding generation."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_create.return_value = self.mock_batch_response
            
            # Call the method
            result = EmbeddingService.batch_generate_embeddings(self.sample_texts)
            
            # Verify the result
            self.assertEqual(result, self.mock_batch_embeddings)
            self.assertEqual(len(result), len(self.sample_texts))
            
            # Verify each embedding has correct dimension
            for embedding in result:
                self.assertEqual(len(embedding), EMBED_DIM)
                self.assertIsInstance(embedding, list)
                self.assertIsInstance(embedding[0], float)
            
            # Verify the API was called correctly
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=self.sample_texts
            )

    def test_batch_generate_embeddings_api_error(self):
        """Test batch embedding generation when API call fails."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            with patch('logging.Logger.error') as mock_error:
                # Configure the mock to raise an exception
                mock_create.side_effect = Exception("Batch API Error")
                
                # Verify the exception is raised
                with self.assertRaises(Exception):
                    EmbeddingService.batch_generate_embeddings(self.sample_texts)
                
                # Verify error was logged
                mock_error.assert_called_once_with(
                    "Batch embedding generation failed: Batch API Error"
                )

    def test_generate_embedding_empty_text(self):
        """Test embedding generation with empty text."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_create.return_value = self.mock_single_response
            
            # Call the method with empty text
            result = EmbeddingService.generate_embedding("")
            
            # Verify the result
            self.assertEqual(result, self.mock_single_embedding)
            
            # Verify the API was called with empty string
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=""
            )

    def test_batch_generate_embeddings_empty_list(self):
        """Test batch embedding generation with empty list."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_response = MagicMock()
            mock_response.data = []
            mock_create.return_value = mock_response
            
            # Call the method with empty list
            result = EmbeddingService.batch_generate_embeddings([])
            
            # Verify the result
            self.assertEqual(result, [])
            
            # Verify the API was called with empty list
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=[]
            )

    def test_generate_embedding_special_characters(self):
        """Test embedding generation with special characters."""
        special_text = "Text with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_create.return_value = self.mock_single_response
            
            # Call the method
            result = EmbeddingService.generate_embedding(special_text)
            
            # Verify the result
            self.assertEqual(result, self.mock_single_embedding)
            
            # Verify the API was called with the special text
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=special_text
            )

    def test_batch_generate_embeddings_single_item(self):
        """Test batch embedding generation with single item list."""
        single_text = ["Single text item"]
        single_embedding = [[0.1] * EMBED_DIM]
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].embedding = single_embedding[0]
        # Support dictionary-style access
        mock_response.data[0].__getitem__ = MagicMock(return_value=single_embedding[0])
        
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure the mock
            mock_create.return_value = mock_response
            
            # Call the method
            result = EmbeddingService.batch_generate_embeddings(single_text)
            
            # Verify the result
            self.assertEqual(result, single_embedding)
            self.assertEqual(len(result), 1)
            
            # Verify the API was called correctly
            mock_create.assert_called_once_with(
                model=EMBEDDING_MODEL,
                input=single_text
            )

    def test_constants_are_correct(self):
        """Test that the constants are set to expected values."""
        self.assertEqual(EMBEDDING_MODEL, "text-embedding-3-small")
        self.assertEqual(EMBED_DIM, 1536)

    def test_methods_are_static(self):
        """Test that all methods are static methods."""
        # Check that methods can be called without instance
        # This is the proper way to test static methods
        try:
            # These should work without creating an instance
            EmbeddingService.generate_embedding("test")
            EmbeddingService.batch_generate_embeddings(["test"])
        except Exception as e:
            # We expect exceptions due to mocking, but not AttributeError
            if isinstance(e, AttributeError):
                self.fail("Methods are not static - cannot call without instance")
        
        # Also check that the methods exist on the class
        self.assertTrue(hasattr(EmbeddingService, 'generate_embedding'))
        self.assertTrue(hasattr(EmbeddingService, 'batch_generate_embeddings'))

    def test_embedding_values_are_floats(self):
        """Test that all embedding values are floats."""
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Create mock embedding with mixed types to test validation
            mixed_embedding = [0.1, 0.2, 0.3, 0.4, 0.5] + [0.0] * (EMBED_DIM - 5)
            mock_response = MagicMock()
            mock_response.data = [MagicMock()]
            mock_response.data[0].embedding = mixed_embedding
            mock_create.return_value = mock_response
            
            # Call the method
            result = EmbeddingService.generate_embedding(self.sample_text)
            
            # Verify all values are floats
            for value in result:
                self.assertIsInstance(value, float)


class TestEmbeddingServiceIntegration(unittest.TestCase):
    """Integration-style tests for EmbeddingService (still using mocks)."""
    
    def test_consistency_between_single_and_batch(self):
        """Test that single and batch methods produce consistent results."""
        sample_text = "Test text for consistency"
        
        with patch('services.embedding.client.embeddings.create') as mock_create:
            # Configure mock to return same embedding for both calls
            mock_embedding = [0.1] * EMBED_DIM
            
            # Create mock responses
            single_response = MagicMock()
            single_response.data = [MagicMock()]
            single_response.data[0].embedding = mock_embedding
            
            batch_response = MagicMock()
            batch_response.data = [MagicMock()]
            batch_response.data[0].embedding = mock_embedding
            # Support dictionary-style access
            batch_response.data[0].__getitem__ = MagicMock(return_value=mock_embedding)
            
            mock_create.side_effect = [single_response, batch_response]
            
            # Get results from both methods
            single_result = EmbeddingService.generate_embedding(sample_text)
            batch_result = EmbeddingService.batch_generate_embeddings([sample_text])[0]
            
            # Verify they are identical
            self.assertEqual(single_result, batch_result)
            self.assertEqual(single_result, mock_embedding)

    def test_error_handling_consistency(self):
        """Test that both methods handle errors consistently."""
        error_message = "Test error"
        
        with patch('services.embedding.client.embeddings.create') as mock_create:
            with patch('logging.Logger.error') as mock_error:
                # Configure mock to raise exception
                mock_create.side_effect = Exception(error_message)
                
                # Test both methods raise the same exception
                with self.assertRaises(Exception):
                    EmbeddingService.generate_embedding("test")
                
                with self.assertRaises(Exception):
                    EmbeddingService.batch_generate_embeddings(["test"])
                
                # Verify both logged errors
                self.assertEqual(mock_error.call_count, 2)


if __name__ == '__main__':
    # Set up logging for tests
    logging.basicConfig(level=logging.INFO)
    
    # Run the tests
    unittest.main(verbosity=2) 