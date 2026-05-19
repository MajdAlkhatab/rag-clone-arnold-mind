# GIFs the model can pull into responses. The "intent" + "tags" fields are what we
# embed, the model retrieves by matching the user's mood / topic, then drops the URL
# into the markdown response.

arnold_gifs = [
    {"id": 1, "title": "Arnold Approval", "intent": "approval",
     "tags": ["arnold", "ok", "approval", "got it"],
     "gif_url": "https://media.giphy.com/media/xGezQibMMkmTS/giphy.gif"},

    {"id": 2, "title": "Arnold Terminator Classic", "intent": "terminator_classic",
     "tags": ["terminator", "arnold", "classic"],
     "gif_url": "https://media.giphy.com/media/12bamrdTlRBOyQ/giphy.gif"},

    {"id": 3, "title": "Arnold Holiday Fun", "intent": "holiday_fun",
     "tags": ["christmas", "jingle all the way", "arnold"],
     "gif_url": "https://media.giphy.com/media/l2YWia4nRCeE92ZJC/giphy.gif"},

    {"id": 4, "title": "Arnold Excited", "intent": "excitement",
     "tags": ["excited", "hype", "energy"],
     "gif_url": "https://media.giphy.com/media/3ofT5xJtfXgV2aqOyI/giphy.gif"},

    {"id": 5, "title": "Arnold Cool Confidence", "intent": "cool_confident",
     "tags": ["cool", "confidence", "arnold"],
     "gif_url": "https://media.giphy.com/media/T9YdDlG5gHj6U/giphy.gif"},

    {"id": 6, "title": "Arnold Intense", "intent": "intensity",
     "tags": ["serious", "focus", "intense"],
     "gif_url": "https://media.giphy.com/media/RPypvDlvWvfy0/giphy.gif"},

    {"id": 7, "title": "Arnold Call To Action", "intent": "call_to_action",
     "tags": ["do it", "action", "reminder"],
     "gif_url": "https://media.giphy.com/media/SXHNorUYlo6VirIshz/giphy.gif"},

    {"id": 8, "title": "Arnold Workout Motivation", "intent": "workout_motivation",
     "tags": ["gym", "workout", "weightlifting"],
     "gif_url": "https://media.giphy.com/media/9vYyNGB3kKU1O/giphy.gif"},

    {"id": 9, "title": "Arnold Flex", "intent": "flex_pride",
     "tags": ["muscles", "flex", "bodybuilding"],
     "gif_url": "https://media.giphy.com/media/g4zFBruwBOHaE/giphy.gif"},

    {"id": 10, "title": "Arnold Montage", "intent": "montage_hype",
     "tags": ["hype", "montage", "energy"],
     "gif_url": "https://media.giphy.com/media/TIvv7HIMVzbZm/giphy.gif"},

    {"id": 11, "title": "Arnold Surprise", "intent": "surprise",
     "tags": ["surprised", "reaction"],
     "gif_url": "https://media.giphy.com/media/4y7peyxlXyBd6/giphy.gif"},

    {"id": 12, "title": "Arnold Smile", "intent": "smile_positive",
     "tags": ["smile", "positive", "friendly"],
     "gif_url": "https://media.giphy.com/media/12gRrmtMlhC9O/giphy.gif"},

    {"id": 13, "title": "Arnold Rage Mode", "intent": "rage_mode",
     "tags": ["commando", "rage", "action"],
     "gif_url": "https://media.giphy.com/media/IsmtGDdJfpWwg/giphy.gif"},
]
