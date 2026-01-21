"""
Tests for StoryBible models.
"""
import pytest
from novel_writer_harness.src.models.story_bible import (
    StoryBible,
    CharacterProfile,
    CharacterRole,
    RelationshipType,
    WorldElement,
    PlotThread
)


class TestCharacterProfile:
    """Test suite for CharacterProfile model."""
    
    def test_character_creation(self):
        """Test creating a basic character profile."""
        character = CharacterProfile(
            name="Jane Doe",
            role=CharacterRole.PROTAGONIST
        )
        
        assert character.name == "Jane Doe"
        assert character.role == CharacterRole.PROTAGONIST
        assert character.id is not None
        assert isinstance(character.aliases, list)
        assert isinstance(character.skills, list)
    
    def test_character_with_details(self):
        """Test character with full details."""
        character = CharacterProfile(
            name="John Smith",
            role=CharacterRole.ANTAGONIST,
            age="45",
            occupation="Detective",
            personality="Cynical but determined",
            skills=["Investigation", "Combat", "Deduction"],
            weaknesses=["Alcohol", "Trust issues"]
        )
        
        assert character.name == "John Smith"
        assert character.age == "45"
        assert character.occupation == "Detective"
        assert len(character.skills) == 3
        assert len(character.weaknesses) == 2
        assert "Investigation" in character.skills
    
    def test_character_arc(self):
        """Test character arc fields."""
        character = CharacterProfile(
            name="Alice",
            arc_type="redemption",
            starting_state="Selfish and isolated",
            ending_state="Selfless and connected"
        )
        
        assert character.arc_type == "redemption"
        assert character.starting_state == "Selfish and isolated"
        assert character.ending_state == "Selfless and connected"
    
    def test_character_to_dict(self):
        """Test character serialization."""
        character = CharacterProfile(
            name="Test Character",
            role=CharacterRole.SUPPORTING,
            age="30"
        )
        
        data = character.to_dict()
        
        assert data["name"] == "Test Character"
        assert data["age"] == "30"
        assert "id" in data


class TestCharacterRole:
    """Test suite for CharacterRole enum."""
    
    def test_all_roles_exist(self):
        """Test all character roles are defined."""
        assert CharacterRole.PROTAGONIST
        assert CharacterRole.ANTAGONIST
        assert CharacterRole.DEUTERAGONIST
        assert CharacterRole.SUPPORTING
        assert CharacterRole.MINOR
        assert CharacterRole.MENTIONED
    
    def test_role_values(self):
        """Test role values."""
        assert CharacterRole.PROTAGONIST.value == "protagonist"
        assert CharacterRole.DEUTERAGONIST.value == "deuteragonist"


class TestRelationshipType:
    """Test suite for RelationshipType enum."""
    
    def test_all_relationships_exist(self):
        """Test all relationship types are defined."""
        assert RelationshipType.FAMILY
        assert RelationshipType.ROMANTIC
        assert RelationshipType.FRIEND
        assert RelationshipType.ENEMY
        assert RelationshipType.RIVAL
        assert RelationshipType.MENTOR
        assert RelationshipType.STUDENT
    
    def test_relationship_values(self):
        """Test relationship values."""
        assert RelationshipType.ROMANTIC.value == "romantic"
        assert RelationshipType.MENTOR.value == "mentor"


class TestStoryBible:
    """Test suite for StoryBible model."""
    
    def test_story_bible_creation(self):
        """Test creating a story bible."""
        bible = StoryBible(title="Test Novel Bible")
        
        assert bible.title == "Test Novel Bible"
        assert bible.id is not None
        assert isinstance(bible.characters, list)
        assert isinstance(bible.world_elements, list)
        assert isinstance(bible.plot_threads, list)
    
    def test_add_character(self):
        """Test adding characters to story bible."""
        bible = StoryBible(title="Test")
        char1 = CharacterProfile(name="Hero", role=CharacterRole.PROTAGONIST)
        char2 = CharacterProfile(name="Villain", role=CharacterRole.ANTAGONIST)
        
        bible.characters.append(char1)
        bible.characters.append(char2)
        
        assert len(bible.characters) == 2
        assert bible.characters[0].name == "Hero"
        assert bible.characters[1].name == "Villain"
    
    def test_find_character_by_name(self):
        """Test finding a character by name."""
        bible = StoryBible(title="Test")
        char = CharacterProfile(name="Alice")
        bible.characters.append(char)
        
        found = bible.find_character_by_name("Alice")
        
        assert found is not None
        assert found.name == "Alice"
    
    def test_find_character_not_found(self):
        """Test finding a character that doesn't exist."""
        bible = StoryBible(title="Test")
        
        found = bible.find_character_by_name("NonExistent")
        
        assert found is None
    
    def test_get_protagonists(self):
        """Test getting all protagonist characters."""
        bible = StoryBible(title="Test")
        bible.characters.append(CharacterProfile(name="Hero1", role=CharacterRole.PROTAGONIST))
        bible.characters.append(CharacterProfile(name="Villain", role=CharacterRole.ANTAGONIST))
        bible.characters.append(CharacterProfile(name="Hero2", role=CharacterRole.PROTAGONIST))
        
        protagonists = bible.get_characters_by_role(CharacterRole.PROTAGONIST)
        
        assert len(protagonists) == 2
        assert all(c.role == CharacterRole.PROTAGONIST for c in protagonists)
