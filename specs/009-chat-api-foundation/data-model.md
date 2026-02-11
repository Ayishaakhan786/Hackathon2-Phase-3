# Data Model: Chat API Foundation

## Entities

### Conversation
Represents a chat session with unique identifier, associated user, and timestamps for creation and last update.

**Fields**:
- `id` (UUID/string): Unique identifier for the conversation
- `user_id` (string): Identifier for the user who owns the conversation
- `created_at` (datetime): Timestamp when the conversation was created
- `updated_at` (datetime): Timestamp when the conversation was last updated

**Validation Rules**:
- `user_id` is required and must be a valid user identifier
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any modification

### Message
Represents an individual message in a conversation with content, sender role (user or assistant), associated conversation and user, and timestamp.

**Fields**:
- `id` (UUID/string): Unique identifier for the message
- `user_id` (string): Identifier for the user who sent the message
- `conversation_id` (string): Reference to the conversation this message belongs to
- `role` (string): Role of the sender ('user' or 'assistant')
- `content` (string): The actual message content
- `created_at` (datetime): Timestamp when the message was created

**Validation Rules**:
- `user_id` is required and must be a valid user identifier
- `conversation_id` is required and must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` is required and must not exceed reasonable length limits
- `created_at` is set automatically on creation

## Relationships

- Conversation (1) → Messages (Many): A conversation can have multiple messages
- Message (Many) → Conversation (1): Each message belongs to exactly one conversation
- User (1) → Conversations (Many): A user can have multiple conversations
- User (1) → Messages (Many): A user can send multiple messages

## State Transitions

None applicable for these data models as they represent static data structures.