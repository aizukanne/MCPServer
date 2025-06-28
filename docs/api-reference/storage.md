# Storage & Messages

These tools provide functionality for message storage and retrieval.

## `get_message_by_sort_id`

Retrieve a specific message by its sort ID.

- **Parameters:**
  - `role` (string): The role of the user (e.g., "user", "assistant").
  - `chat_id` (string): The ID of the chat.
  - `sort_id` (string): The sort ID of the message.
- **Returns:**
  - A JSON object containing the message.

## `get_messages_in_range`

Get all messages within a specific time range.

- **Parameters:**
  - `chat_id` (string): The ID of the chat.
  - `start_sort_id` (string): The starting sort ID of the range.
  - `end_sort_id` (string): The ending sort ID of the range.
- **Returns:**
  - A JSON object containing a list of messages.

## `get_users`

Get information about a specific user or all users.

- **Parameters:**
  - `user_id` (string, optional): The ID of the user.
- **Returns:**
  - A JSON object containing user information.

## `get_channels`

Get information about a specific channel or all channels.

- **Parameters:**
  - `id` (string, optional): The ID of the channel.
- **Returns:**
  - A JSON object containing channel information.

## `manage_mute_status`

Manage the mute status of a channel.

- **Parameters:**
  - `chat_id` (string): The ID of the chat.
  - `status` (boolean, optional): The new mute status.
- **Returns:**
  - A JSON object confirming the status change.