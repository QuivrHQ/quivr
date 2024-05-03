import pytest
from unittest.mock import patch
from ..knowledge_brain_qa import generate_source, get_or_generate_url, create_source_object

# Assuming generate_source, get_or_generate_url, and create_source_object are in the module named 'module_path'

@pytest.fixture
def test_documents():
    return [
        {'file_name': 'doc1.pdf', 'is_url': False, 'original_file_name': 'Original Doc 1', 'page_content': 'Content of doc1'},
        {'file_name': 'doc2.pdf', 'is_url': True, 'original_file_name': 'http://example.com/doc2', 'page_content': 'Content of doc2'}
    ]

@pytest.fixture
def brain_id():
    return 'brain-123'

@pytest.fixture
def citations():
    return [0]  # Assume only the first document is cited

def test_generate_source(test_documents, brain_id, citations):
    with patch('modules.brain.knowledge_brain_qa.generate_file_signed_url') as mock_generate_file_signed_url:
        mock_generate_file_signed_url.return_value = {'signedURL': 'http://signedurl.com/doc1'}
        
        sources = generate_source(test_documents, brain_id, citations)

        print('sources: ', sources)

        assert len(sources) == 1  # Check correct number of sources generated
        assert sources[0].source_url == 'http://signedurl.com/doc1'
        assert sources[0].name == 'doc1.pdf'
        assert sources[0].type == 'file'

def test_get_or_generate_url_with_existing_url(test_documents, brain_id):
    url_cache = {}
    url = get_or_generate_url(test_documents[1], brain_id, url_cache)
    
    assert url == 'http://example.com/doc2'  # Test URL from document directly used

def test_create_source_object(test_documents):
    doc = test_documents[0]
    source = create_source_object(doc, 'file', 'http://signedurl.com/doc1')
    
    assert source.name == 'doc1.pdf'
    assert source.type == 'file'
    assert source.source_url == 'http://signedurl.com/doc1'
    assert source.original_file_name == 'doc1.pdf'

def test_generate_source_no_citations(test_documents, brain_id):
    with patch('modules.brain.knowledge_brain_qa.generate_file_signed_url') as mock_generate_file_signed_url:
        mock_generate_file_signed_url.return_value = {'signedURL': 'http://signedurl.com/doc1'}
        
        sources = generate_source(test_documents, brain_id)

        assert len(sources) == 2  # Check that sources are generated for all documents since no citations filter is applied