"""
Tests for Context models and management.
"""
import pytest
from novel_writer_harness.src.models.context import (
    ContextConfig,
    ContextMode,
    ContextBlock,
    AssembledContext,
    WritingTask
)


class TestContextMode:
    """Test suite for ContextMode enum."""
    
    def test_all_modes_exist(self):
        """Test all context modes are defined."""
        assert ContextMode.MINIMAL
        assert ContextMode.STANDARD
        assert ContextMode.COMPREHENSIVE
        assert ContextMode.CUSTOM
    
    def test_mode_values(self):
        """Test mode values."""
        assert ContextMode.MINIMAL.value == "minimal"
        assert ContextMode.COMPREHENSIVE.value == "comprehensive"


class TestWritingTask:
    """Test suite for WritingTask enum."""
    
    def test_all_tasks_exist(self):
        """Test all writing tasks are defined."""
        assert WritingTask.CONTINUE
        assert WritingTask.SUGGEST
        assert WritingTask.REWRITE
        assert WritingTask.EXPAND
        assert WritingTask.CONDENSE
        assert WritingTask.DIALOGUE
        assert WritingTask.DESCRIBE
        assert WritingTask.OUTLINE
        assert WritingTask.BRAINSTORM
        assert WritingTask.ANALYZE
        assert WritingTask.EDIT
    
    def test_task_values(self):
        """Test task values."""
        assert WritingTask.CONTINUE.value == "continue"
        assert WritingTask.DIALOGUE.value == "dialogue"


class TestContextConfig:
    """Test suite for ContextConfig model."""
    
    def test_default_config(self):
        """Test creating config with defaults."""
        config = ContextConfig()
        
        assert config.mode == ContextMode.STANDARD
        assert config.max_tokens == 100000
        assert config.reserve_output_tokens == 4000
        assert config.include_story_bible is True
        assert config.include_genre_guidance is True
        assert config.include_recent_chapters == 2
    
    def test_custom_config(self):
        """Test creating custom config."""
        config = ContextConfig(
            mode=ContextMode.MINIMAL,
            max_tokens=50000,
            include_story_bible=False,
            include_recent_chapters=1
        )
        
        assert config.mode == ContextMode.MINIMAL
        assert config.max_tokens == 50000
        assert config.include_story_bible is False
        assert config.include_recent_chapters == 1
    
    def test_custom_mode_with_inclusions(self):
        """Test CUSTOM mode with specific inclusions."""
        config = ContextConfig(
            mode=ContextMode.CUSTOM,
            included_character_ids=["char1", "char2"],
            included_chapter_numbers=[1, 2, 3]
        )
        
        assert config.mode == ContextMode.CUSTOM
        assert len(config.included_character_ids) == 2
        assert len(config.included_chapter_numbers) == 3
        assert "char1" in config.included_character_ids


class TestContextBlock:
    """Test suite for ContextBlock model."""
    
    def test_context_block_creation(self):
        """Test creating a context block."""
        block = ContextBlock(
            content="This is test content",
            source="test_chapter_1",
            priority=5,
            category="chapter"
        )
        
        assert block.content == "This is test content"
        assert block.source == "test_chapter_1"
        assert block.priority == 5
        assert block.category == "chapter"
    
    def test_token_estimation(self):
        """Test token estimation."""
        # 20 chars = approximately 5 tokens (4 chars per token)
        block = ContextBlock(
            content="0123456789" * 2,  # 20 chars
            source="test",
            priority=1
        )
        
        estimated = block.estimate_tokens()
        
        assert estimated == 5
        assert block.token_estimate == 5
    
    def test_token_estimation_large(self):
        """Test token estimation with larger text."""
        # 400 chars = approximately 100 tokens
        block = ContextBlock(
            content="x" * 400,
            source="test",
            priority=1
        )
        
        estimated = block.estimate_tokens()
        
        assert estimated == 100
        assert block.token_estimate == 100


class TestAssembledContext:
    """Test suite for AssembledContext model."""
    
    def test_assembled_context_creation(self):
        """Test creating assembled context."""
        context = AssembledContext(
            system_prompt="You are a helpful writing assistant.",
            user_prompt="Continue the story from here."
        )
        
        assert context.system_prompt == "You are a helpful writing assistant."
        assert context.user_prompt == "Continue the story from here."
        assert isinstance(context.context_blocks, list)
        assert len(context.context_blocks) == 0
    
    def test_add_context_blocks(self):
        """Test adding context blocks."""
        context = AssembledContext()
        
        block1 = ContextBlock(content="Block 1", source="source1", priority=1)
        block2 = ContextBlock(content="Block 2", source="source2", priority=2)
        
        context.context_blocks.append(block1)
        context.context_blocks.append(block2)
        
        assert len(context.context_blocks) == 2
        assert context.context_blocks[0].content == "Block 1"
        assert context.context_blocks[1].content == "Block 2"
    
    def test_calculate_total_tokens(self):
        """Test calculating total tokens in context."""
        context = AssembledContext()
        
        block1 = ContextBlock(content="x" * 400, source="1", priority=1)
        block1.estimate_tokens()
        block2 = ContextBlock(content="x" * 200, source="2", priority=2)
        block2.estimate_tokens()
        
        context.context_blocks.append(block1)
        context.context_blocks.append(block2)
        
        total = context.calculate_total_tokens()
        
        assert total == 150  # 100 + 50 tokens
