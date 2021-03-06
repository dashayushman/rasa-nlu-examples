import pytest
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from rasa_nlu_examples.fallback import FasttextLanguageFallbackClassifier
from rasa.shared.nlu.constants import TEXT, INTENT
from rasa.shared.nlu.training_data.message import Message

tokenizer = WhitespaceTokenizer()


@pytest.mark.parametrize(
    "txt,lang", [("ik spreek een taal", "nl"), ("je parle une langue", "fr")]
)
def test_detect_obvious_cases(txt, lang):
    config_dict = {
        "expected_language": "en",
        "threshold": 0.7,
        "min_tokens": 2,
        "min_chars": 8,
        "intent_triggered": f"detected_{lang}",
        "cache_dir": "tests/data/fasttext",
        "file": "lid.176.ftz",
    }
    ft_lang = FasttextLanguageFallbackClassifier(config_dict)
    message = Message({TEXT: txt, INTENT: {"name": "assigned_before"}})
    tokenizer.process(message=message)
    ft_lang.process(message=message)
    assert message.get(INTENT)["name"] == f"detected_{lang}"


@pytest.mark.parametrize(
    "txt,lang", [("i am speaking english", "en"), ("this too should pass", "en")]
)
def test_no_change_on_english(txt, lang):
    config_dict = {
        "expected_language": "en",
        "threshold": 0.3,
        "min_tokens": 2,
        "min_chars": 8,
        "intent_triggered": "is_not_english",
        "cache_dir": "tests/data/fasttext",
        "file": "lid.176.ftz",
    }
    ft_lang = FasttextLanguageFallbackClassifier(config_dict)
    message = Message({TEXT: txt, INTENT: {"name": "assigned_before"}})
    tokenizer.process(message=message)
    ft_lang.process(message=message)
    assert message.get(INTENT)["name"] == "assigned_before"


@pytest.mark.parametrize(
    "txt,lang", [("ik spreek een taal", "nl"), ("je parle une langue", "fr")]
)
def test_no_change_when_protected(txt, lang):
    config_dict = {
        "expected_language": "en",
        "threshold": 0.3,
        "min_tokens": 2,
        "min_chars": 8,
        "intent_triggered": "is_not_english",
        "cache_dir": "tests/data/fasttext",
        "file": "lid.176.ftz",
        "protected_intents": ["assigned_before"],
    }
    ft_lang = FasttextLanguageFallbackClassifier(config_dict)
    message = Message({TEXT: txt, INTENT: {"name": "assigned_before"}})
    tokenizer.process(message=message)
    ft_lang.process(message=message)
    assert message.get(INTENT)["name"] == "assigned_before"


@pytest.mark.parametrize(
    "txt,lang", [("ik spreek een taal", "nl"), ("je parle une langue", "fr")]
)
def test_no_change_when_too_short_tokens(txt, lang):
    config_dict = {
        "expected_language": "en",
        "threshold": 0.3,
        "min_tokens": 5,
        "min_chars": 8,
        "intent_triggered": "is_not_english",
        "cache_dir": "tests/data/fasttext",
        "file": "lid.176.ftz",
        "protected_intents": ["assigned_before"],
    }
    ft_lang = FasttextLanguageFallbackClassifier(config_dict)
    message = Message({TEXT: txt, INTENT: {"name": "assigned_before"}})
    tokenizer.process(message=message)
    ft_lang.process(message=message)
    assert message.get(INTENT)["name"] == "assigned_before"


@pytest.mark.parametrize(
    "txt,lang", [("ik spreek een taal", "nl"), ("je parle une langue", "fr")]
)
def test_no_change_when_too_short_chars(txt, lang):
    config_dict = {
        "expected_language": "en",
        "threshold": 0.3,
        "min_tokens": 1,
        "min_chars": 100,
        "intent_triggered": "is_not_english",
        "cache_dir": "tests/data/fasttext",
        "file": "lid.176.ftz",
        "protected_intents": ["assigned_before"],
    }
    ft_lang = FasttextLanguageFallbackClassifier(config_dict)
    message = Message({TEXT: txt, INTENT: {"name": "assigned_before"}})
    tokenizer.process(message=message)
    ft_lang.process(message=message)
    assert message.get(INTENT)["name"] == "assigned_before"
