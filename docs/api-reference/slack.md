# Slack Integration

These tools provide integration with Slack.

## `send_file_to_slack`

Upload a file to a Slack channel.

- **Parameters:**
  - `file_path` (string): The path to the file to upload.
  - `chat_id` (string): The ID of the Slack channel.
  - `title` (string): The title of the file.
  - `ts` (string, optional): The timestamp of a message to reply to.
- **Returns:**
  - A JSON object confirming the file upload.

## `update_slack_users`

Synchronize user data from Slack.

- **Returns:**
  - A JSON object confirming the synchronization.

## `update_slack_conversations`

Synchronize channel data from Slack.

- **Returns:**
  - A JSON object confirming the synchronization.