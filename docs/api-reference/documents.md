# Document Management

These tools provide functionality for document management.

## `send_as_pdf`

Convert text to a PDF and upload it to Slack.

- **Parameters:**
  - `text` (string): The text to convert.
  - `chat_id` (string): The ID of the Slack channel.
  - `title` (string): The title of the PDF.
  - `ts` (string, optional): The timestamp of a message to reply to.
- **Returns:**
  - A JSON object confirming the upload.

## `list_files`

List files in an S3 bucket.

- **Parameters:**
  - `folder_prefix` (string, optional): The prefix of the folder to list.
- **Returns:**
  - A JSON object containing a list of files.

## `get_embedding`

Generate text embeddings using a specified model.

- **Parameters:**
  - `text` (string): The text to embed.
  - `model` (string, optional): The model to use for generating the embedding.
- **Returns:**
  - A JSON object containing the text embedding.