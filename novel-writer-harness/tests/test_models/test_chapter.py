"""
Tests for Chapter and Scene models.
"""
import pytest
from datetime import datetime
from novel_writer_harness.src.models.chapter import (
    Chapter,
    Scene,
    ChapterStatus,
    POVType
)


class TestScene:
    """Test suite for Scene model."""
    
    def test_scene_creation(self):
        """Test creating a basic scene."""
        scene = Scene(title="Opening Scene", content="It was a dark and stormy night...")
        
        assert scene.title == "Opening Scene"
        assert scene.content == "It was a dark and stormy night..."
        assert scene.id is not None
        assert isinstance(scene.created_at, datetime)
        assert scene.status == ChapterStatus.OUTLINE
    
    def test_scene_word_count(self):
        """Test word count calculation."""
        scene = Scene(content="The quick brown fox jumps over the lazy dog")
        count = scene.update_word_count()
        
        assert count == 9
        assert scene.word_count == 9
    
    def test_scene_word_count_empty(self):
        """Test word count with empty content."""
        scene = Scene(content="")
        count = scene.update_word_count()
        
        assert count == 0
        assert scene.word_count == 0
    
    def test_scene_to_dict(self):
        """Test scene serialization."""
        scene = Scene(
            title="Test Scene",
            content="Test content",
            pov_character="Jane Doe",
            location="Library"
        )
        
        data = scene.to_dict()
        
        assert data["title"] == "Test Scene"
        assert data["content"] == "Test content"
        assert data["pov_character"] == "Jane Doe"
        assert data["location"] == "Library"
        assert "id" in data
    
    def test_scene_metadata(self):
        """Test scene metadata fields."""
        scene = Scene(
            pov_character="John Smith",
            location="Downtown",
            time_in_story="Day 1, Morning",
            goal="Find the artifact",
            conflict="Guards blocking the way",
            disaster_or_resolution="Arrested"
        )
        
        assert scene.pov_character == "John Smith"
        assert scene.location == "Downtown"
        assert scene.goal == "Find the artifact"
        assert scene.conflict == "Guards blocking the way"
        assert scene.disaster_or_resolution == "Arrested"


class TestChapter:
    """Test suite for Chapter model."""
    
    def test_chapter_creation(self):
        """Test creating a basic chapter."""
        chapter = Chapter(number=1, title="Chapter One")
        
        assert chapter.number == 1
        assert chapter.title == "Chapter One"
        assert chapter.id is not None
        assert len(chapter.scenes) == 0
        assert chapter.status == ChapterStatus.OUTLINE
    
    def test_chapter_add_scene(self):
        """Test adding scenes to a chapter."""
        chapter = Chapter(number=1, title="Chapter One")
        scene1 = Scene(title="Scene 1")
        scene2 = Scene(title="Scene 2")
        
        chapter.scenes.append(scene1)
        chapter.scenes.append(scene2)
        
        assert len(chapter.scenes) == 2
        assert chapter.scenes[0].title == "Scene 1"
        assert chapter.scenes[1].title == "Scene 2"
    
    def test_chapter_word_count(self):
        """Test chapter word count calculation."""
        chapter = Chapter(number=1, title="Test")
        chapter.scenes.append(Scene(content="One two three four five"))
        chapter.scenes.append(Scene(content="Six seven eight"))
        
        total = chapter.calculate_word_count()
        
        assert total == 8  # 5 + 3 words
        assert chapter.word_count == 8
    
    def test_chapter_status_progression(self):
        """Test chapter status can be updated."""
        chapter = Chapter(number=1, title="Test")
        
        assert chapter.status == ChapterStatus.OUTLINE
        
        chapter.status = ChapterStatus.DRAFT
        assert chapter.status == ChapterStatus.DRAFT
        
        chapter.status = ChapterStatus.FINAL
        assert chapter.status == ChapterStatus.FINAL


class TestPOVType:
    """Test suite for POVType enum."""
    
    def test_pov_types_exist(self):
        """Test all POV types are defined."""
        assert POVType.FIRST_PERSON
        assert POVType.SECOND_PERSON
        assert POVType.THIRD_LIMITED
        assert POVType.THIRD_OMNISCIENT
        assert POVType.MULTIPLE
    
    def test_pov_type_values(self):
        """Test POV type values."""
        assert POVType.FIRST_PERSON.value == "first_person"
        assert POVType.THIRD_LIMITED.value == "third_limited"


class TestChapterStatus:
    """Test suite for ChapterStatus enum."""
    
    def test_status_types_exist(self):
        """Test all status types are defined."""
        assert ChapterStatus.OUTLINE
        assert ChapterStatus.DRAFT
        assert ChapterStatus.REVISION_1
        assert ChapterStatus.REVISION_2
        assert ChapterStatus.POLISHED
        assert ChapterStatus.FINAL
    
    def test_status_values(self):
        """Test status values."""
        assert ChapterStatus.OUTLINE.value == "outline"
        assert ChapterStatus.FINAL.value == "final"
