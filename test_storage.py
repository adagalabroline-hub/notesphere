from database.storage import load_notes, save_notes

print("Initial:", load_notes())

save_notes([
    {"title": "Test Note", "content": "Hello NoteSphere"}
])

print("After save:", load_notes())