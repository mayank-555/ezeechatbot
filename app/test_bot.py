import requests

# Step 1: Upload text to your bot
upload_response = requests.post(
    "http://127.0.0.1:8000/upload",
    json={
        "text": "AI is transforming industries. It helps automate tasks. Businesses use AI to improve decision-making."
    }
)

# Get the bot_id from the upload response
bot_id = upload_response.json().get("bot_id")
print("Bot ID:", bot_id)

# Step 2: Query the bot
query_response = requests.post(
    "http://127.0.0.1:8000/query",
    json={
        "bot_id": bot_id,
        "question": "Where is AI used?"
    }
)

# Print the query results
print("Query Results:", query_response.json())